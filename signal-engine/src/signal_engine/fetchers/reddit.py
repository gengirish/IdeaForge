"""Reddit ingestion via PullPush API."""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

import httpx

from signal_engine.models import FetchResult, RawSignal, SourceType, ThesisConfig

logger = logging.getLogger(__name__)

PULLPUSH_URL = "https://api.pullpush.io/reddit/search/submission/"


def _reddit_search_terms(reddit_cfg: dict, thesis: ThesisConfig) -> list[str]:
    """PullPush breaks on Lucene OR chains — fetch one term at a time."""
    if keywords := reddit_cfg.get("keywords"):
        return [str(k).strip() for k in keywords if str(k).strip()]
    if query := reddit_cfg.get("query", "").strip():
        if " OR " in query.upper():
            return thesis.keywords[:8] if thesis.keywords else [query.split(" OR ")[0].strip()]
        return [query]
    return [k for k in thesis.keywords[:8] if k] or ["recruiting"]


def _matches_keywords(text: str, terms: list[str]) -> bool:
    if not terms:
        return True
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def _parse_reddit_item(item: dict, sub: str) -> RawSignal | None:
    post_id = item.get("id") or item.get("name", "")
    title = item.get("title") or ""
    body = item.get("selftext") or item.get("body") or ""
    if not title and not body:
        return None
    author = item.get("author") or ""
    permalink = item.get("permalink") or ""
    url = f"https://reddit.com{permalink}" if permalink.startswith("/") else permalink
    return RawSignal(
        source=SourceType.REDDIT,
        source_id=str(post_id),
        url=url or f"https://reddit.com/r/{sub}",
        title=title,
        body=body[:8000],
        author=author,
        fetched_at=datetime.now(UTC),
    )


async def _pullpush_search(
    client: httpx.AsyncClient,
    *,
    subreddit: str,
    query: str | None,
    limit: int,
) -> list[dict]:
    """Search PullPush without `after` — epoch cutoffs exclude all hits when the index lags."""
    params: dict = {
        "subreddit": subreddit,
        "size": min(limit, 100),
        "sort": "desc",
        "sort_type": "created_utc",
    }
    if query:
        params["q"] = query

    resp = await client.get(PULLPUSH_URL, params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])


def _within_recency_window(item: dict, after: int) -> bool:
    created = item.get("created_utc")
    if created is None:
        return True
    return int(created) >= after


def _apply_recency(
    items: list[dict],
    after: int,
    *,
    sub: str,
    stale_subs: list[str],
) -> list[dict]:
    recent = [item for item in items if _within_recency_window(item, after)]
    if items and not recent:
        if sub not in stale_subs:
            stale_subs.append(sub)
        return items
    return recent


async def fetch_reddit(
    thesis: ThesisConfig,
    *,
    client: httpx.AsyncClient | None = None,
    limit: int = 25,
) -> FetchResult:
    reddit_cfg = thesis.sources.get("reddit", {})
    subreddits: list[str] = reddit_cfg.get("subreddits", [])
    terms = _reddit_search_terms(reddit_cfg, thesis)
    days_back = int(reddit_cfg.get("days_back", 14))
    after = int((datetime.now(UTC) - timedelta(days=days_back)).timestamp())
    fallback_listing = reddit_cfg.get("fallback_listing", True)

    signals: list[RawSignal] = []
    seen: set[str] = set()
    owns_client = client is None
    if client is None:
        client = httpx.AsyncClient(timeout=30.0)

    def add_signal(signal: RawSignal | None) -> None:
        if signal is None:
            return
        key = signal.source_id
        if key in seen:
            return
        seen.add(key)
        signals.append(signal)

    try:
        stale_subs: list[str] = []

        for sub in subreddits:
            for term in terms:
                try:
                    items = await _pullpush_search(
                        client, subreddit=sub, query=term, limit=limit
                    )
                except Exception as exc:
                    logger.warning("Reddit fetch failed r/%s q=%r: %s", sub, term, exc)
                    continue
                for item in _apply_recency(items, after, sub=sub, stale_subs=stale_subs):
                    add_signal(_parse_reddit_item(item, sub))

        if not signals and fallback_listing:
            logger.info("Reddit keyword fetch empty — falling back to subreddit listing + local filter")
            for sub in subreddits:
                try:
                    items = await _pullpush_search(
                        client, subreddit=sub, query=None, limit=limit
                    )
                except Exception as exc:
                    logger.warning("Reddit listing fallback failed r/%s: %s", sub, exc)
                    continue
                for item in _apply_recency(items, after, sub=sub, stale_subs=stale_subs):
                    parsed = _parse_reddit_item(item, sub)
                    if parsed is None:
                        continue
                    haystack = f"{parsed.title} {parsed.body}"
                    if _matches_keywords(haystack, terms):
                        add_signal(parsed)

        if stale_subs:
            logger.warning(
                "PullPush index appears stale for r/%s — included posts older than %dd",
                ", ".join(stale_subs),
                days_back,
            )
    finally:
        if owns_client:
            await client.aclose()

    logger.info("Reddit fetched %d signals (%d subreddits, %d terms)", len(signals), len(subreddits), len(terms))
    return FetchResult(signals=signals, source=SourceType.REDDIT)
