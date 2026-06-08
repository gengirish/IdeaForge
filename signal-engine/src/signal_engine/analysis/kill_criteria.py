"""Kill criteria evaluation from thesis YAML."""

from __future__ import annotations

from pydantic import BaseModel

from signal_engine.models import ScoredSignal, ThesisConfig, ThesisFit


class KillCriteriaAlert(BaseModel):
    description: str
    window_days: int
    threshold: int
    current_value: int
    triggered: bool
    action: str = "review"


def evaluate_kill_criteria(
    thesis: ThesisConfig,
    *,
    window_signals: list[ScoredSignal],
    interview_worthy_count: int,
) -> list[KillCriteriaAlert]:
    """Evaluate each kill criterion from thesis config against recent signals."""
    alerts: list[KillCriteriaAlert] = []

    for criterion in thesis.kill_criteria:
        description = str(criterion.get("description", "Unnamed criterion"))
        threshold = int(criterion.get("threshold", 0))
        window_days = int(criterion.get("window_days", 7))

        current = _measure_criterion(
            description,
            window_signals,
            interview_worthy_count=interview_worthy_count,
        )
        triggered = _is_triggered(current, threshold, description)

        alerts.append(
            KillCriteriaAlert(
                description=description,
                window_days=window_days,
                threshold=threshold,
                current_value=current,
                triggered=triggered,
                action="pause thesis" if triggered else "continue",
            )
        )

    return alerts


def _measure_criterion(
    description: str,
    signals: list[ScoredSignal],
    *,
    interview_worthy_count: int,
) -> int:
    desc = description.lower()

    if "contradict" in desc or "work fine" in desc or "manual phone" in desc:
        return sum(1 for s in signals if s.scorecard.thesis_fit == ThesisFit.CONTRADICTS)

    if "interview-worthy" in desc or "zero interview" in desc:
        return interview_worthy_count

    if "contradicts" in desc:
        return sum(1 for s in signals if s.scorecard.thesis_fit == ThesisFit.CONTRADICTS)

    return len(signals)


def _is_triggered(current: int, threshold: int, description: str) -> bool:
    desc = description.lower()

    # "Zero interview-worthy" → trigger when count <= threshold (0)
    if "zero interview" in desc or "interview-worthy" in desc:
        return current <= threshold

    # "3+ signals say X" → trigger when count >= threshold
    return current >= threshold
