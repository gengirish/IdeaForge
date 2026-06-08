"""Persist signals and scorecards."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta

import asyncpg

from signal_engine.models import (
    PainFrequency,
    PersonaFit,
    RawSignal,
    Scorecard,
    ScoredSignal,
    SourceType,
    ThesisFit,
    WouldPay,
    YesNo,
)

SELECT_SCORED = """
SELECT
    s.source, s.source_id, s.url, s.title, s.body, s.author, s.fetched_at,
    s.thesis_name,
    sc.pain_real, sc.pain_frequency, sc.pain_expensive, sc.already_paying,
    sc.persona_fit, sc.would_pay, sc.three_yes, sc.thesis_fit, sc.urgency,
    sc.rationale, sc.disqualifier_hit, sc.interview_worthy, sc.scored_at
FROM signals s
JOIN scorecards sc ON sc.signal_id = s.id
WHERE s.thesis_name = $1
  AND sc.scored_at >= $2
  AND ($3::timestamptz IS NULL OR sc.scored_at < $3)
ORDER BY sc.scored_at DESC
"""


def content_hash(signal: RawSignal) -> str:
    payload = f"{signal.source}:{signal.source_id}:{signal.title}:{signal.body[:500]}"
    return hashlib.sha256(payload.encode()).hexdigest()


def _row_to_scored(row: asyncpg.Record) -> ScoredSignal:
    raw = RawSignal(
        source=SourceType(row["source"]),
        source_id=row["source_id"],
        url=row["url"],
        title=row["title"],
        body=row["body"],
        author=row["author"] or "",
        fetched_at=row["fetched_at"],
    )
    scorecard = Scorecard(
        pain_real=YesNo(row["pain_real"]),
        pain_frequency=PainFrequency(row["pain_frequency"]),
        pain_expensive=YesNo(row["pain_expensive"]),
        already_paying=YesNo(row["already_paying"]),
        persona_fit=PersonaFit(row["persona_fit"]),
        would_pay=WouldPay(row["would_pay"]),
        three_yes=YesNo(row["three_yes"]),
        thesis_fit=ThesisFit(row["thesis_fit"]),
        urgency=row["urgency"],
        rationale=row["rationale"] or "",
        disqualifier_hit=row["disqualifier_hit"],
    )
    return ScoredSignal(raw=raw, scorecard=scorecard, thesis_name=row["thesis_name"])


async def upsert_signal(
    conn: asyncpg.Connection,
    signal: RawSignal,
    thesis_name: str,
) -> int:
    h = signal.content_hash or content_hash(signal)
    row = await conn.fetchrow(
        """
        INSERT INTO signals (source, source_id, url, title, body, author, content_hash, thesis_name, fetched_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (source, source_id) DO UPDATE SET
            title = EXCLUDED.title,
            body = EXCLUDED.body,
            fetched_at = EXCLUDED.fetched_at
        RETURNING id
        """,
        signal.source.value,
        signal.source_id,
        signal.url,
        signal.title,
        signal.body,
        signal.author,
        h,
        thesis_name,
        signal.fetched_at,
    )
    return int(row["id"])


async def upsert_scorecard(conn: asyncpg.Connection, signal_id: int, scored: ScoredSignal) -> None:
    sc = scored.scorecard
    await conn.execute(
        """
        INSERT INTO scorecards (
            signal_id, pain_real, pain_frequency, pain_expensive, already_paying,
            persona_fit, would_pay, three_yes, thesis_fit, urgency, rationale,
            disqualifier_hit, interview_worthy
        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
        ON CONFLICT (signal_id) DO UPDATE SET
            pain_real = EXCLUDED.pain_real,
            pain_frequency = EXCLUDED.pain_frequency,
            pain_expensive = EXCLUDED.pain_expensive,
            already_paying = EXCLUDED.already_paying,
            persona_fit = EXCLUDED.persona_fit,
            would_pay = EXCLUDED.would_pay,
            three_yes = EXCLUDED.three_yes,
            thesis_fit = EXCLUDED.thesis_fit,
            urgency = EXCLUDED.urgency,
            rationale = EXCLUDED.rationale,
            disqualifier_hit = EXCLUDED.disqualifier_hit,
            interview_worthy = EXCLUDED.interview_worthy,
            scored_at = NOW()
        """,
        signal_id,
        sc.pain_real.value,
        sc.pain_frequency.value,
        sc.pain_expensive.value,
        sc.already_paying.value,
        sc.persona_fit.value,
        sc.would_pay.value,
        sc.three_yes.value,
        sc.thesis_fit.value,
        sc.urgency,
        sc.rationale,
        sc.disqualifier_hit,
        sc.interview_worthy,
    )


async def save_scored_signal(pool: asyncpg.Pool, scored: ScoredSignal) -> int:
    async with pool.acquire() as conn:
        signal_id = await upsert_signal(conn, scored.raw, scored.thesis_name)
        await upsert_scorecard(conn, signal_id, scored)
        return signal_id


async def fetch_scored_in_window(
    pool: asyncpg.Pool,
    thesis_name: str,
    *,
    since: datetime,
    until: datetime | None = None,
) -> list[ScoredSignal]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(SELECT_SCORED, thesis_name, since, until)
    return [_row_to_scored(row) for row in rows]


async def fetch_scored_last_n_days(
    pool: asyncpg.Pool,
    thesis_name: str,
    days: int,
) -> list[ScoredSignal]:
    since = datetime.now(UTC) - timedelta(days=days)
    return await fetch_scored_in_window(pool, thesis_name, since=since)


async def count_interview_worthy_in_window(
    pool: asyncpg.Pool,
    thesis_name: str,
    days: int,
) -> int:
    since = datetime.now(UTC) - timedelta(days=days)
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT COUNT(*) AS cnt
            FROM signals s
            JOIN scorecards sc ON sc.signal_id = s.id
            WHERE s.thesis_name = $1
              AND sc.scored_at >= $2
              AND sc.interview_worthy = TRUE
            """,
            thesis_name,
            since,
        )
    return int(row["cnt"])
