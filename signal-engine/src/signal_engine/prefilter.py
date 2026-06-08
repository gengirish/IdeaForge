"""Cheap pre-LLM gate: rank by keyword relevance and cap batch size."""

from __future__ import annotations

from signal_engine.models import RawSignal, ThesisConfig


def keyword_relevance(signal: RawSignal, keywords: list[str]) -> float:
    """Higher = more thesis keyword overlap (title weighted 3× body)."""
    if not keywords:
        return 0.0
    title = signal.title.lower()
    body = signal.body.lower()
    score = 0.0
    for keyword in keywords:
        term = keyword.lower().strip()
        if not term:
            continue
        if term in title:
            score += 3.0
        if term in body:
            score += 1.0
    return score


def select_signals_for_scoring(
    signals: list[RawSignal],
    thesis: ThesisConfig,
    max_signals: int,
) -> tuple[list[RawSignal], int]:
    """Return top-N signals by relevance (then recency). Skipped count is the remainder."""
    if max_signals <= 0 or len(signals) <= max_signals:
        return signals, 0

    ranked = sorted(
        signals,
        key=lambda s: (keyword_relevance(s, thesis.keywords), s.fetched_at.timestamp()),
        reverse=True,
    )
    selected = ranked[:max_signals]
    return selected, len(signals) - len(selected)
