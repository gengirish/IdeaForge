"""LangGraph node implementations for the signal pipeline."""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal

import yaml

from signal_engine.analysis.contradictions import ContradictionAlert, detect_contradictions
from signal_engine.analysis.delta import DeltaSummary, compute_delta
from signal_engine.analysis.kill_criteria import KillCriteriaAlert, evaluate_kill_criteria
from signal_engine.config import get_settings
from signal_engine.db import get_pool, init_schema
from signal_engine.digest import render_digest, write_digest
from signal_engine.fetchers import fetch_hn, fetch_reddit
from signal_engine.graph.state import PipelineState
from signal_engine.models import RawSignal, ScoredSignal, ThesisConfig
from signal_engine.repository import (
    count_interview_worthy_in_window,
    fetch_scored_in_window,
    fetch_scored_last_n_days,
    save_scored_signal,
)
from signal_engine.email.digest_mail import send_digest_email
from signal_engine.scorer import score_signals_batch

logger = logging.getLogger(__name__)


def load_thesis(path: Path) -> ThesisConfig:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ThesisConfig.model_validate(data)


async def node_load_thesis(state: PipelineState) -> PipelineState:
    path = Path(state["thesis_path"])
    thesis = load_thesis(path)
    return {
        "thesis": thesis.model_dump(mode="json"),
        "step": "loaded",
    }


async def node_fetch_sources(state: PipelineState) -> PipelineState:
    thesis = ThesisConfig.model_validate(state["thesis"])
    reddit_result, hn_result = await asyncio.gather(
        fetch_reddit(thesis),
        fetch_hn(thesis),
    )
    signals = reddit_result.signals + hn_result.signals
    logger.info("Fetched %d raw signals", len(signals))
    return {
        "raw_signals": [s.model_dump(mode="json") for s in signals],
        "step": "fetched",
    }


async def node_dedupe(state: PipelineState) -> PipelineState:
    seen: set[str] = set()
    unique: list[dict] = []
    for item in state.get("raw_signals", []):
        key = f"{item['source']}:{item['source_id']}"
        if key not in seen:
            seen.add(key)
            unique.append(item)
    logger.info("Deduped to %d unique signals", len(unique))
    return {"raw_signals": unique, "step": "deduped"}


async def node_score_batch(state: PipelineState) -> PipelineState:
    thesis = ThesisConfig.model_validate(state["thesis"])
    signals = [RawSignal.model_validate(s) for s in state.get("raw_signals", [])]
    settings = get_settings()

    batch = await score_signals_batch(signals, thesis, settings=settings)
    errors = list(state.get("errors", [])) + batch.errors

    return {
        "scored_signals": [s.model_dump(mode="json") for s in batch.scored],
        "errors": errors,
        "step": "scored" if not batch.errors else "score_partial",
    }


async def node_persist(state: PipelineState) -> PipelineState:
    scored_items = [ScoredSignal.model_validate(s) for s in state.get("scored_signals", [])]
    pool = await get_pool()
    try:
        await init_schema(pool)
        for item in scored_items:
            await save_scored_signal(pool, item)
    finally:
        await pool.close()
    return {"step": "persisted"}


async def node_analyze_retention(state: PipelineState) -> PipelineState:
    """Phase 2: delta view, contradiction alerts, kill criteria."""
    thesis = ThesisConfig.model_validate(state["thesis"])
    now = datetime.now(UTC)
    last_24h_start = now - timedelta(hours=24)
    prior_24h_start = now - timedelta(hours=48)

    contradiction_threshold = 3
    for criterion in thesis.kill_criteria:
        desc = str(criterion.get("description", "")).lower()
        if "work fine" in desc or "contradict" in desc:
            contradiction_threshold = int(criterion.get("threshold", 3))
            break

    try:
        pool = await get_pool()
        try:
            last_24h = await fetch_scored_in_window(
                pool, thesis.name, since=last_24h_start
            )
            prior_24h = await fetch_scored_in_window(
                pool,
                thesis.name,
                since=prior_24h_start,
                until=last_24h_start,
            )
            window_7d = await fetch_scored_last_n_days(pool, thesis.name, 7)
            iw_14d = await count_interview_worthy_in_window(pool, thesis.name, 14)
        finally:
            await pool.close()
    except Exception as exc:
        logger.warning("Retention analysis skipped (DB unavailable): %s", exc)
        return {"step": "analyze_skipped"}

    delta = compute_delta(last_24h=last_24h, prior_24h=prior_24h, now=now)
    contradiction = detect_contradictions(
        window_7d,
        window_days=7,
        alert_threshold=contradiction_threshold,
    )
    kill_alerts = evaluate_kill_criteria(
        thesis,
        window_signals=window_7d,
        interview_worthy_count=iw_14d,
    )

    logger.info(
        "Analysis: %d new (24h), %d contradictions (7d), %d kill criteria triggered",
        len(delta.new_since_prior_day),
        contradiction.count,
        sum(1 for a in kill_alerts if a.triggered),
    )

    return {
        "delta_summary": delta.model_dump(mode="json"),
        "contradiction_alert": contradiction.model_dump(mode="json"),
        "kill_criteria_alerts": [a.model_dump(mode="json") for a in kill_alerts],
        "step": "analyzed",
    }


async def node_render_digest(state: PipelineState) -> PipelineState:
    thesis = ThesisConfig.model_validate(state["thesis"])
    scored = [ScoredSignal.model_validate(s) for s in state.get("scored_signals", [])]

    delta = None
    if state.get("delta_summary"):
        delta = DeltaSummary.model_validate(state["delta_summary"])

    contradiction = None
    if state.get("contradiction_alert"):
        contradiction = ContradictionAlert.model_validate(state["contradiction_alert"])

    kill_criteria = None
    if state.get("kill_criteria_alerts"):
        kill_criteria = [
            KillCriteriaAlert.model_validate(a) for a in state["kill_criteria_alerts"]
        ]

    content = render_digest(
        thesis,
        scored,
        delta=delta,
        contradiction=contradiction,
        kill_criteria=kill_criteria,
    )
    return {"digest_content": content, "step": "rendered"}


async def node_send_digest_email(state: PipelineState) -> PipelineState:
    """Send markdown digest via AgentMail (skips gracefully if unconfigured)."""
    if state.get("dry_run"):
        return {"email_sent": False, "email_skip_reason": "dry-run", "step": "email_skipped"}

    content = state.get("digest_content", "")
    if not content:
        return {"email_sent": False, "email_skip_reason": "no digest content", "step": "email_skipped"}

    thesis = ThesisConfig.model_validate(state["thesis"])
    result = await send_digest_email(thesis=thesis, markdown_body=content)

    if result.ok:
        logger.info("Digest email sent%s", f" (id={result.message_id})" if result.message_id else "")
        return {"email_sent": True, "email_skip_reason": "", "step": "email_sent"}

    logger.info("Digest email skipped: %s", result.reason)
    return {"email_sent": False, "email_skip_reason": result.reason, "step": "email_skipped"}


async def node_write_digest(state: PipelineState) -> PipelineState:
    settings = get_settings()
    thesis_path = Path(state["thesis_path"])
    digest_path = Path(settings.digest_output_path)
    if not digest_path.is_absolute():
        digest_path = (thesis_path.parent.parent / digest_path).resolve()

    write_digest(digest_path, state.get("digest_content", ""))
    logger.info("Digest written to %s", digest_path)
    return {"digest_path": str(digest_path), "step": "complete"}


def route_after_dedupe(state: PipelineState) -> Literal["render_digest", "score_batch"]:
    if state.get("dry_run") or state.get("skip_scoring"):
        return "render_digest"
    return "score_batch"
