"""Reddit ingestion via PullPush API."""

from __future__ import annotations

from datetime import UTC, datetime

import httpx

from signal_engine.models import FetchResult, RawSignal, SourceType, ThesisConfig

PULLPUSH_URL = "https://api.pullpush.io/reddit/search/submission/"


async def fetch_reddit(
    thesis: ThesisConfig,
    *,
    client: httpx.AsyncClient | None = None,
    limit: int = 25,
) -> FetchResult:
    reddit_cfg = thesis.sources.get("reddit", {})
    subreddits: list[str] = reddit_cfg.get("subreddits", [])
    query: str = reddit_cfg.get("query", " OR ".join(thesis.keywords[:5]))

    signals: list[RawSignal] = []
    owns_client = client is None
    if client is None:
        client = httpx.AsyncClient(timeout=30.0)

    try:
        for sub in subreddits:
            params = {
                "subreddit": sub,
                "q": query,
                "size": min(limit, 100),
                "sort": "desc",
                "sort_type": "created_utc",
            }
            resp = await client.get(PULLPUSH_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("data", []):
                post_id = item.get("id") or item.get("name", "")
                title = item.get("title") or ""
                body = item.get("selftext") or item.get("body") or ""
                author = item.get("author") or ""
                permalink = item.get("permalink") or ""
                url = f"https://reddit.com{permalink}" if permalink.startswith("/") else permalink

                if not title and not body:
                    continue

                signals.append(
                    RawSignal(
                        source=SourceType.REDDIT,
                        source_id=str(post_id),
                        url=url or f"https://reddit.com/r/{sub}",
                        title=title,
                        body=body[:8000],
                        author=author,
                        fetched_at=datetime.now(UTC),
                    )
                )
    finally:
        if owns_client:
            await client.aclose()

    return FetchResult(signals=signals, source=SourceType.REDDIT)
