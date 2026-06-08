"""Contradiction alerts — signals that weaken the thesis."""

from __future__ import annotations

from pydantic import BaseModel, Field

from signal_engine.models import ScoredSignal, ThesisFit


class ContradictionAlert(BaseModel):
    window_days: int
    count: int
    threshold: int = 3
    triggered: bool = False
    samples: list[ScoredSignal] = Field(default_factory=list)
    message: str = ""


def detect_contradictions(
    signals: list[ScoredSignal],
    *,
    window_days: int = 7,
    alert_threshold: int = 3,
) -> ContradictionAlert:
    """Flag when enough recent signals contradict the thesis."""
    contradicts = [s for s in signals if s.scorecard.thesis_fit == ThesisFit.CONTRADICTS]
    count = len(contradicts)
    triggered = count >= alert_threshold

    message = ""
    if triggered:
        message = (
            f"{count} signals in the last {window_days} days contradict your thesis "
            f"(threshold: {alert_threshold}). Review before doubling down."
        )

    return ContradictionAlert(
        window_days=window_days,
        count=count,
        threshold=alert_threshold,
        triggered=triggered,
        samples=contradicts[:5],
        message=message,
    )
