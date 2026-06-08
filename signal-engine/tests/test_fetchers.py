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
            "reddit": {
                "subreddits": ["recruiting"],
                "keywords": ["phone screen", "ATS"],
                "days_back": 14,
            },
            "hn": {
                "query": "recruiting screening",
                "days_back": 30,
                "tags": "story,comment",
            },
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
async def test_fetch_reddit_dedupes_across_keywords(thesis: ThesisConfig) -> None:
    respx.get("https://api.pullpush.io/reddit/search/submission/").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "t3_same",
                        "title": "Same post",
                        "selftext": "ATS pain",
                        "permalink": "/r/recruiting/comments/same/",
                    }
                ]
            },
        )
    )

    result = await fetch_reddit(thesis, limit=5)
    assert len(result.signals) == 1


@respx.mock
@pytest.mark.asyncio
async def test_fetch_reddit_fallback_filters_listing(thesis: ThesisConfig) -> None:
    route = respx.get("https://api.pullpush.io/reddit/search/submission/")

    def handler(request):
        if request.url.params.get("q"):
            return Response(200, json={"data": []})
        return Response(
            200,
            json={
                "data": [
                    {
                        "id": "t3_fb",
                        "title": "Our ATS is broken",
                        "selftext": "manual screens all week",
                        "permalink": "/r/recruiting/comments/fb/",
                    },
                    {
                        "id": "t3_skip",
                        "title": "Random meme",
                        "selftext": "nothing hiring related",
                        "permalink": "/r/recruiting/comments/skip/",
                    },
                ]
            },
        )

    route.mock(side_effect=handler)

    result = await fetch_reddit(thesis, limit=5)
    assert len(result.signals) == 1
    assert "ATS" in result.signals[0].title


@pytest.mark.asyncio
async def test_hn_search_terms_splits_multiword(thesis: ThesisConfig) -> None:
    from signal_engine.fetchers.hn import _hn_search_terms

    terms = _hn_search_terms(thesis.sources["hn"], thesis)
    assert len(terms) >= 2
    assert "recruiting" in terms


@respx.mock
@pytest.mark.asyncio
async def test_fetch_hn_parses_stories_and_comments(thesis: ThesisConfig) -> None:
    def handler(request):
        tag = request.url.params.get("tags")
        if tag == "story":
            return Response(
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
        return Response(
            200,
            json={
                "hits": [
                    {
                        "objectID": "99999",
                        "comment_text": "We still do phone screens manually every week",
                        "author": "ta_lead",
                    }
                ]
            },
        )

    respx.get("https://hn.algolia.com/api/v1/search").mock(side_effect=handler)

    result = await fetch_hn(thesis, limit=5)
    assert result.source == SourceType.HN
    assert len(result.signals) == 2
    assert result.signals[0].source_id == "12345"
    assert "phone screens" in result.signals[1].title
