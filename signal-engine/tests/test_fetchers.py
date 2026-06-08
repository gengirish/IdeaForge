import pytest
import respx
from httpx import Response

from signal_engine.fetchers.hn import fetch_hn
from signal_engine.fetchers.reddit import fetch_reddit
from signal_engine.models import SourceType, ThesisConfig


@pytest.fixture
def thesis() -> ThesisConfig:
    return ThesisConfig(
        name="Test Thesis",
        vertical="test",
        icp={"titles": ["TA Lead"]},
        problem_hypothesis="Manual screening is painful",
        keywords=["phone screen"],
        disqualifiers=["job seeker"],
        sources={
            "reddit": {"subreddits": ["recruiting"], "query": "phone screen"},
            "hn": {"query": "recruiting screening"},
        },
    )


@respx.mock
@pytest.mark.asyncio
async def test_fetch_reddit_parses_posts(thesis: ThesisConfig) -> None:
    respx.get("https://api.pullpush.io/reddit/search/submission/").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "t3_abc",
                        "title": "Phone screens taking forever",
                        "selftext": "We do 50 screens/week manually",
                        "author": "ta_lead",
                        "permalink": "/r/recruiting/comments/abc/phone_screens/",
                    }
                ]
            },
        )
    )

    result = await fetch_reddit(thesis, limit=5)
    assert result.source == SourceType.REDDIT
    assert len(result.signals) == 1
    assert result.signals[0].title == "Phone screens taking forever"
    assert "reddit.com" in result.signals[0].url


@respx.mock
@pytest.mark.asyncio
async def test_fetch_hn_parses_hits(thesis: ThesisConfig) -> None:
    respx.get("https://hn.algolia.com/api/v1/search").mock(
        return_value=Response(
            200,
            json={
                "hits": [
                    {
                        "objectID": "12345",
                        "title": "Ask HN: Structured interviews for hiring?",
                        "url": "https://example.com",
                        "author": "founder1",
                    }
                ]
            },
        )
    )

    result = await fetch_hn(thesis, limit=5)
    assert result.source == SourceType.HN
    assert len(result.signals) == 1
    assert result.signals[0].source_id == "12345"
