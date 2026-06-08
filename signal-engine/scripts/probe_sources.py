"""Quick probe of Reddit/HN fetch APIs — run: uv run python scripts/probe_sources.py"""

import asyncio
from datetime import UTC, datetime, timedelta

import httpx

PULLPUSH = "https://api.pullpush.io/reddit/search/submission/"
ALGOLIA = "https://hn.algolia.com/api/v1/search"


async def probe() -> None:
    since14 = int((datetime.now(UTC) - timedelta(days=14)).timestamp())
    since30 = int((datetime.now(UTC) - timedelta(days=30)).timestamp())

    async with httpx.AsyncClient(timeout=30) as c:
        print("=== Reddit (PullPush) ===")
        for sub in ["recruiting", "humanresources", "recruitinghell"]:
            r = await c.get(PULLPUSH, params={"subreddit": sub, "q": "phone screen", "size": 5})
            print(f"  r/{sub} q='phone screen': {len(r.json().get('data', []))} hits")

        r = await c.get(PULLPUSH, params={"subreddit": "recruiting", "size": 5})
        data = r.json().get("data", [])
        print(f"  r/recruiting listing: {len(data)} hits")
        if data:
            newest = max(int(d.get("created_utc", 0)) for d in data)
            print(f"  newest created_utc in sample: {newest} ({datetime.fromtimestamp(newest, UTC).date()})")

        r = await c.get(
            PULLPUSH,
            params={"subreddit": "recruiting", "size": 5, "after": since14},
        )
        print(f"  r/recruiting with API after=14d epoch: {len(r.json().get('data', []))} (often 0 — index lag)")

        print("\n=== HN (Algolia) ===")
        for q in [
            "recruiting hiring screening interview",
            "recruiting OR hiring OR screening OR interview",
            "recruiting",
        ]:
            r = await c.get(
                ALGOLIA,
                params={
                    "query": q,
                    "tags": "story",
                    "numericFilters": f"created_at_i>{since30}",
                    "hitsPerPage": 5,
                },
            )
            print(f"  stories q={q!r}: {len(r.json().get('hits', []))} hits")

        r = await c.get(
            ALGOLIA,
            params={
                "query": "recruiting OR hiring",
                "tags": "comment",
                "numericFilters": f"created_at_i>{since30}",
                "hitsPerPage": 5,
            },
        )
        print(f"  comments (30d, OR query): {len(r.json().get('hits', []))} hits")


if __name__ == "__main__":
    asyncio.run(probe())
