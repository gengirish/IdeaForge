"""Hacker News ingestion via Algolia API."""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

import httpx

from signal_engine.models import FetchResult, RawSignal, SourceType, ThesisConfig

logger = logging.getLogger(__name__)

ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"


def _hn_search_terms(hn_cfg: dict, thesis: ThesisConfig) -> list[str]:
    if queries := hn_cfg.get("queries"):
        return [str(q).strip() for q in queries if str(q).strip()]
    if query := hn_cfg.get("query", "").strip():
        if " OR " in query.upper():
            return [t.strip() for t in query.split(" OR ") if t.strip()]
        words = query.split()
        if len(words) > 1:
            return words
        return [query]
    return [k for k in thesis.keywords[:6] if k] or ["recruiting"]


def _hn_tags(hn_cfg: dict) -> list[str]:
    raw = hn_cfg.get("tags", ["story", "comment"])
    if isinstance(raw, str):
        return [t.strip() for t in raw.split(",") if t.strip()]
    return [str(t).strip() for t in raw if str(t).strip()] or ["story"]


def _parse_hn_hit(hit: dict, tag: str) -> RawSignal | None:
    object_id = hit.get("objectID", "")
    title = hit.get("title") or hit.get("story_title") or ""
    url = hit.get("url") or f"https://news.ycombinator.com/item?id={object_id}"
    body = hit.get("story_text") or hit.get("comment_text") or ""
    author = hit.get("author") or ""

    if tag == "comment" and not title:
        snippet = body.replace("\n", " ").strip()[:120]
        title = snippet or f"HN comment by {author or 'anonymous'}"

    if not title and not body:
        return None

    return RawSignal(
        source=SourceType.HN,
        source_id=str(object_id),
        url=url,
        title=title,
        body=body[:8000],
        author=author,
        fetched_at=datetime.now(UTC),
    )


async def fetch_hn(
    thesis: ThesisConfig,
    *,
    client: httpx.AsyncClient | None = None,
    limit: int = 25,
    days_back: int | None = None,
) -> FetchResult:
    hn_cfg = thesis.sources.get("hn", {})
    terms = _hn_search_terms(hn_cfg, thesis)
    window_days = int(days_back if days_back is not None else hn_cfg.get("days_back", 30))
    since = int((datetime.now(UTC) - timedelta(days=window_days)).timestamp())
    tags = _hn_tags(hn_cfg)

    signals: list[RawSignal] = []
    seen: set[str] = set()
    owns_client = client is None
    if client is None:
        client = httpx.AsyncClient(timeout=30.0)

    try:
        for term in terms:
            for tag in tags:
                params = {
                    "query": term,
                    "tags": tag,
                    "numericFilters": f"created_at_i>{since}",
                    "hitsPerPage": min(limit, 100),
                }
                resp = await client.get(ALGOLIA_URL, params=params)
                resp.raise_for_status()
                hits = resp.json().get("hits", [])

                for hit in hits:
                    signal = _parse_hn_hit(hit, tag)
                    if signal is None or signal.source_id in seen:
                        continue
                    seen.add(signal.source_id)
                    signals.append(signal)
    finally:
        if owns_client:
            await client.aclose()

    logger.info(
        "HN fetched %d signals (%dd window, %d terms, tags=%s)",
        len(signals),
        window_days,
        len(terms),
        tags,
    )
    return FetchResult(signals=signals, source=SourceType.HN)
