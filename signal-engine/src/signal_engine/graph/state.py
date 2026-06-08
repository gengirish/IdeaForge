"""LangGraph pipeline state."""

from __future__ import annotations

from typing import TypedDict


class PipelineState(TypedDict, total=False):
    thesis_path: str
    dry_run: bool
    skip_scoring: bool
    thesis: dict
    raw_signals: list[dict]
    scored_signals: list[dict]
    delta_summary: dict
    contradiction_alert: dict
    kill_criteria_alerts: list[dict]
    digest_path: str
    digest_content: str
    email_sent: bool
    email_skip_reason: str
    step: str
    errors: list[str]
    prefilter_total: int
    prefilter_selected: int
    prefilter_skipped: int
