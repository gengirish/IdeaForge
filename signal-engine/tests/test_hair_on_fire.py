"""Tests for hair-on-fire aggregation."""

from datetime import UTC, datetime

from signal_engine.analysis.hair_on_fire import filter_hair_on_fire, render_hair_on_fire_analysis
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


def _scored(*, urgency: int = 4, frequency: PainFrequency = PainFrequency.WEEKLY) -> ScoredSignal:
    return ScoredSignal(
        raw=RawSignal(
            source=SourceType.HN,
            source_id="1",
            url="https://news.ycombinator.com/item?id=1",
            title="ATS integration keeps breaking",
            body="We lose hours every week.",
        ),
        scorecard=Scorecard(
            pain_real=YesNo.YES,
            pain_frequency=frequency,
            pain_expensive=YesNo.YES,
            already_paying=YesNo.YES,
            persona_fit=PersonaFit.BUYER,
            would_pay=WouldPay.YES,
            three_yes=YesNo.YES,
            thesis_fit=ThesisFit.SUPPORTS,
            urgency=urgency,
            rationale="Weekly ATS pain with budget already spent on workarounds.",
        ),
        thesis_name="Recruiting / TA — Vettd dogfood",
    )


def test_hair_on_fire_requires_weekly_urgent_pain() -> None:
    assert _scored().scorecard.hair_on_fire is True
    assert _scored(urgency=3).scorecard.hair_on_fire is False
    assert _scored(frequency=PainFrequency.MONTHLY).scorecard.hair_on_fire is False


def test_filter_hair_on_fire_returns_matching_signals() -> None:
    hot = _scored()
    mild = _scored(urgency=2)
    assert filter_hair_on_fire([hot, mild]) == [hot]


def test_render_hair_on_fire_analysis_lists_signals() -> None:
    thesis = ThesisConfig(
        name="Recruiting / TA — Vettd dogfood",
        vertical="recruiting_ta",
        icp={},
        problem_hypothesis="screening pain",
    )
    markdown = render_hair_on_fire_analysis(
        thesis,
        [_scored(), _scored(urgency=2)],
        generated_at=datetime(2026, 6, 23, 12, 0, tzinfo=UTC),
    )
    assert "Hair-on-fire signals:** 1" in markdown
    assert "ATS integration keeps breaking" in markdown
    assert "Weekly ATS pain" in markdown
