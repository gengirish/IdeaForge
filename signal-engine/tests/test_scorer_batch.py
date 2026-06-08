import asyncio
from unittest.mock import patch

import pytest

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
from signal_engine.scorer import score_signals_batch


@pytest.fixture
def thesis() -> ThesisConfig:
    return ThesisConfig(
        name="Test",
        vertical="test",
        icp={},
        problem_hypothesis="Manual screening hurts",
    )


def _scorecard() -> Scorecard:
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
        rationale="Clear buyer pain",
    )


def _signal(idx: int) -> RawSignal:
    return RawSignal(
        source=SourceType.REDDIT,
        source_id=f"id-{idx}",
        url=f"https://example.com/{idx}",
        title=f"Signal {idx}",
        body="body",
    )


@pytest.mark.asyncio
async def test_score_signals_batch_aggregates_successes(thesis: ThesisConfig) -> None:
    signals = [_signal(i) for i in range(3)]

    async def fake_score(signal: RawSignal, thesis_cfg: ThesisConfig, *, settings=None):
        return ScoredSignal(raw=signal, scorecard=_scorecard(), thesis_name=thesis_cfg.name)

    with patch("signal_engine.scorer.score_signal", side_effect=fake_score):
        result = await score_signals_batch(signals, thesis, concurrency=2)

    assert len(result.scored) == 3
    assert result.errors == []
    assert result.interview_worthy_count == 3


@pytest.mark.asyncio
async def test_score_signals_batch_aggregates_failures(thesis: ThesisConfig) -> None:
    signals = [_signal(i) for i in range(3)]

    async def fake_score(signal: RawSignal, thesis_cfg: ThesisConfig, *, settings=None):
        if signal.source_id == "id-1":
            raise RuntimeError("provider down")
        return ScoredSignal(raw=signal, scorecard=_scorecard(), thesis_name=thesis_cfg.name)

    with patch("signal_engine.scorer.score_signal", side_effect=fake_score):
        result = await score_signals_batch(signals, thesis, concurrency=3)

    assert len(result.scored) == 2
    assert len(result.errors) == 1
    assert "score:id-1:" in result.errors[0]


@pytest.mark.asyncio
async def test_score_signals_batch_respects_concurrency(thesis: ThesisConfig) -> None:
    signals = [_signal(i) for i in range(8)]
    active = 0
    max_active = 0
    lock = asyncio.Lock()

    async def slow_score(signal: RawSignal, thesis_cfg: ThesisConfig, *, settings=None):
        nonlocal active, max_active
        async with lock:
            active += 1
            max_active = max(max_active, active)
        await asyncio.sleep(0.05)
        async with lock:
            active -= 1
        return ScoredSignal(raw=signal, scorecard=_scorecard(), thesis_name=thesis_cfg.name)

    with patch("signal_engine.scorer.score_signal", side_effect=slow_score):
        result = await score_signals_batch(signals, thesis, concurrency=4)

    assert len(result.scored) == 8
    assert max_active <= 4
    assert max_active >= 2
