"""Tests for Phase 2 retention analysis."""

from datetime import UTC, datetime

from signal_engine.analysis.contradictions import detect_contradictions
from signal_engine.analysis.delta import compute_delta
from signal_engine.analysis.kill_criteria import evaluate_kill_criteria
from signal_engine.models import (
    PainFrequency,
    PersonaFit,
    RawSignal,
    Scorecard,
    ScoredSignal,
    SourceType,
    ThesisConfig,
    ThesisFit,
    WouldPay,
    YesNo,
)


def _scored(
    source_id: str,
    *,
    thesis_fit: ThesisFit = ThesisFit.SUPPORTS,
    interview_worthy: bool = False,
    title: str = "Test signal",
) -> ScoredSignal:
    return ScoredSignal(
        raw=RawSignal(
            source=SourceType.REDDIT,
            source_id=source_id,
            url=f"https://reddit.com/{source_id}",
            title=title,
            body="body",
        ),
        scorecard=Scorecard(
            pain_real=YesNo.YES if interview_worthy else YesNo.NO,
            pain_frequency=PainFrequency.WEEKLY,
            pain_expensive=YesNo.YES,
            already_paying=YesNo.NO,
            persona_fit=PersonaFit.BUYER if interview_worthy else PersonaFit.NOT_FIT,
            would_pay=WouldPay.YES if interview_worthy else WouldPay.NO,
            three_yes=YesNo.YES if interview_worthy else YesNo.NO,
            thesis_fit=thesis_fit,
            urgency=4 if interview_worthy else 2,
            rationale="test",
        ),
        thesis_name="Recruiting / TA",
    )


def test_compute_delta_finds_new_signals() -> None:
    prior = [_scored("a"), _scored("b")]
    last = [_scored("a"), _scored("b"), _scored("c", interview_worthy=True)]

    delta = compute_delta(
        last_24h=last,
        prior_24h=prior,
        now=datetime(2026, 6, 7, tzinfo=UTC),
    )

    assert len(delta.new_since_prior_day) == 1
    assert delta.new_since_prior_day[0].raw.source_id == "c"
    assert len(delta.new_interview_worthy) == 1


def test_detect_contradictions_triggers_at_threshold() -> None:
    signals = [_scored(str(i), thesis_fit=ThesisFit.CONTRADICTS) for i in range(3)]
    alert = detect_contradictions(signals, alert_threshold=3)
    assert alert.triggered is True
    assert alert.count == 3
    assert "contradict" in alert.message.lower()


def test_evaluate_kill_criteria_zero_interview_worthy() -> None:
    thesis = ThesisConfig(
        name="Test",
        vertical="test",
        icp={},
        problem_hypothesis="pain",
        kill_criteria=[
            {
                "description": "Zero interview-worthy signals for 14 days",
                "threshold": 0,
                "window_days": 14,
            }
        ],
    )
    alerts = evaluate_kill_criteria(
        thesis,
        window_signals=[],
        interview_worthy_count=0,
    )
    assert len(alerts) == 1
    assert alerts[0].triggered is True


def test_evaluate_kill_criteria_contradiction_count() -> None:
    thesis = ThesisConfig(
        name="Test",
        vertical="test",
        icp={},
        problem_hypothesis="pain",
        kill_criteria=[
            {
                "description": "3+ signals/week say manual phone screens work fine",
                "threshold": 3,
                "window_days": 7,
            }
        ],
    )
    signals = [_scored(str(i), thesis_fit=ThesisFit.CONTRADICTS) for i in range(2)]
    alerts = evaluate_kill_criteria(
        thesis,
        window_signals=signals,
        interview_worthy_count=1,
    )
    assert alerts[0].triggered is False

    signals.append(_scored("x", thesis_fit=ThesisFit.CONTRADICTS))
    alerts = evaluate_kill_criteria(
        thesis,
        window_signals=signals,
        interview_worthy_count=1,
    )
    assert alerts[0].triggered is True
