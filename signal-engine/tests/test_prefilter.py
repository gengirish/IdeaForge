from datetime import UTC, datetime, timedelta

from signal_engine.models import RawSignal, SourceType, ThesisConfig
from signal_engine.prefilter import keyword_relevance, select_signals_for_scoring


def _signal(title: str, body: str = "", *, offset_hours: int = 0) -> RawSignal:
    return RawSignal(
        source=SourceType.HN,
        source_id=title,
        url="https://example.com",
        title=title,
        body=body,
        fetched_at=datetime.now(UTC) - timedelta(hours=offset_hours),
    )


def test_keyword_relevance_weights_title() -> None:
    thesis = ThesisConfig(
        name="T",
        vertical="v",
        icp={},
        problem_hypothesis="p",
        keywords=["SOC 2", "audit"],
    )
    high = _signal("SOC 2 audit nightmare", "weekly pain")
    low = _signal("Random post", "SOC 2 mentioned once")
    assert keyword_relevance(high, thesis.keywords) > keyword_relevance(low, thesis.keywords)


def test_select_signals_for_scoring_caps_and_ranks() -> None:
    thesis = ThesisConfig(
        name="T",
        vertical="v",
        icp={},
        problem_hypothesis="p",
        keywords=["SOC 2", "compliance"],
    )
    signals = [
        _signal("Unrelated meme", "nothing here"),
        _signal("SOC 2 compliance pain", "audit evidence manual", offset_hours=1),
        _signal("Compliance audit backlog", "GRC team drowning", offset_hours=0),
        _signal("SOC 2 again", "questionnaire hell", offset_hours=2),
    ]

    selected, skipped = select_signals_for_scoring(signals, thesis, max_signals=2)

    assert len(selected) == 2
    assert skipped == 2
    assert all("SOC" in s.title or "Compliance" in s.title for s in selected)


def test_select_signals_no_cap_when_under_limit() -> None:
    thesis = ThesisConfig(name="T", vertical="v", icp={}, problem_hypothesis="p")
    signals = [_signal("a"), _signal("b")]

    selected, skipped = select_signals_for_scoring(signals, thesis, max_signals=50)

    assert len(selected) == 2
    assert skipped == 0
