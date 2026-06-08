"""Hacker News ingestion via Algolia API."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx

from signal_engine.models import FetchResult, RawSignal, SourceType, ThesisConfig

ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"


async def fetch_hn(
    thesis: ThesisConfig,
    *,
    client: httpx.AsyncClient | None = None,
    limit: int = 25,
    days_back: int = 7,
) -> FetchResult:
    hn_cfg = thesis.sources.get("hn", {})
    query: str = hn_cfg.get("query", " OR ".join(thesis.keywords[:5]))
    since = int((datetime.now(UTC) - timedelta(days=days_back)).timestamp())

    signals: list[RawSignal] = []
    owns_client = client is None
    if client is None:
        client = httpx.AsyncClient(timeout=30.0)

    try:
        params = {
            "query": query,
            "tags": "story",
            "numericFilters": f"created_at_i>{since}",
            "hitsPerPage": min(limit, 100),
        }
        resp = await client.get(ALGOLIA_URL, params=params)
        resp.raise_for_status()
        hits = resp.json().get("hits", [])

        for hit in hits:
            object_id = hit.get("objectID", "")
            title = hit.get("title") or ""
            url = hit.get("url") or f"https://news.ycombinator.com/item?id={object_id}"
            body = hit.get("story_text") or hit.get("comment_text") or ""
            author = hit.get("author") or ""

            if not title:
                continue

            signals.append(
                RawSignal(
                    source=SourceType.HN,
                    source_id=str(object_id),
                    url=url,
                    title=title,
                    body=body[:8000],
                    author=author,
                    fetched_at=datetime.now(UTC),
                )
            )
    finally:
        if owns_client:
            await client.aclose()

    return FetchResult(signals=signals, source=SourceType.HN)
