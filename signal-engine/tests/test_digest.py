"""Tests for digest Phase 2 sections."""

from datetime import UTC, datetime

from signal_engine.analysis.contradictions import ContradictionAlert
from signal_engine.analysis.delta import DeltaSummary
from signal_engine.analysis.kill_criteria import KillCriteriaAlert
from signal_engine.digest import render_digest
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


def test_render_digest_includes_phase2_sections() -> None:
    thesis = ThesisConfig(
        name="Recruiting TA",
        vertical="recruiting_ta",
        icp={},
        problem_hypothesis="Screening pain",
        competitors=[],
        linkedin_manual_queries=[],
    )
    scored = ScoredSignal(
        raw=RawSignal(
            source=SourceType.REDDIT,
            source_id="1",
            url="https://reddit.com/1",
            title="Manual screens killing us",
            body="50/week",
        ),
        scorecard=Scorecard(
            pain_real=YesNo.YES,
            pain_frequency=PainFrequency.WEEKLY,
            pain_expensive=YesNo.YES,
            already_paying=YesNo.NO,
            persona_fit=PersonaFit.BUYER,
            would_pay=WouldPay.YES,
            three_yes=YesNo.YES,
            thesis_fit=ThesisFit.SUPPORTS,
            urgency=5,
            rationale="Weekly backlog described.",
        ),
        thesis_name=thesis.name,
        llm_provider="NVIDIA NIM",
        llm_model="meta/llama-4-maverick-17b-128e-instruct",
    )

    delta = DeltaSummary(
        since=datetime(2026, 6, 6, tzinfo=UTC),
        new_since_prior_day=[scored],
        new_interview_worthy=[scored],
        total_last_24h=1,
        interview_worthy_last_24h=1,
    )
    contradiction = ContradictionAlert(
        window_days=7,
        count=3,
        threshold=3,
        triggered=True,
        message="3 signals contradict your thesis.",
    )
    kill = [
        KillCriteriaAlert(
            description="Zero interview-worthy signals for 14 days",
            window_days=14,
            threshold=0,
            current_value=1,
            triggered=False,
        )
    ]

    md = render_digest(
        thesis,
        [scored],
        delta=delta,
        contradiction=contradiction,
        kill_criteria=kill,
        generated_at=datetime(2026, 6, 7, tzinfo=UTC),
    )

    assert "## Since yesterday" in md
    assert "## Contradiction alerts" in md
    assert "## Kill criteria" in md
    assert "NVIDIA NIM" in md
