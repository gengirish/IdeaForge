import pytest

from signal_engine.models import (
    PainFrequency,
    PersonaFit,
    RawSignal,
    Scorecard,
    SourceType,
    ThesisFit,
    WouldPay,
    YesNo,
)


@pytest.fixture
def sample_scorecard() -> Scorecard:
    return Scorecard(
        pain_real=YesNo.YES,
        pain_frequency=PainFrequency.WEEKLY,
        pain_expensive=YesNo.YES,
        already_paying=YesNo.NO,
        persona_fit=PersonaFit.BUYER,
        would_pay=WouldPay.YES,
        three_yes=YesNo.YES,
        thesis_fit=ThesisFit.SUPPORTS,
        urgency=4,
        rationale="TA lead describes weekly manual phone screen backlog.",
    )


def test_interview_worthy_gate_passes(sample_scorecard: Scorecard) -> None:
    assert sample_scorecard.interview_worthy is True


def test_interview_worthy_fails_on_disqualifier(sample_scorecard: Scorecard) -> None:
    sample_scorecard.disqualifier_hit = "job seeker venting"
    assert sample_scorecard.interview_worthy is False


def test_interview_worthy_fails_on_low_urgency(sample_scorecard: Scorecard) -> None:
    sample_scorecard.urgency = 2
    assert sample_scorecard.interview_worthy is False


def test_raw_signal_defaults() -> None:
    signal = RawSignal(
        source=SourceType.REDDIT,
        source_id="abc123",
        url="https://reddit.com/r/test",
        title="Test",
        body="Body",
    )
    assert signal.author == ""
