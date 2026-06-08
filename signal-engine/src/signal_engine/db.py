"""Postgres connection and schema."""

from __future__ import annotations

import asyncpg

from signal_engine.config import get_settings

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS signals (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    author TEXT DEFAULT '',
    content_hash TEXT NOT NULL,
    thesis_name TEXT NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (source, source_id)
);

CREATE TABLE IF NOT EXISTS scorecards (
    id SERIAL PRIMARY KEY,
    signal_id INTEGER NOT NULL REFERENCES signals(id) ON DELETE CASCADE,
    pain_real TEXT NOT NULL,
    pain_frequency TEXT NOT NULL,
    pain_expensive TEXT NOT NULL,
    already_paying TEXT NOT NULL,
    persona_fit TEXT NOT NULL,
    would_pay TEXT NOT NULL,
    three_yes TEXT NOT NULL,
    thesis_fit TEXT NOT NULL,
    urgency INTEGER NOT NULL,
    rationale TEXT DEFAULT '',
    disqualifier_hit TEXT,
    interview_worthy BOOLEAN NOT NULL DEFAULT FALSE,
    scored_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (signal_id)
);

CREATE INDEX IF NOT EXISTS idx_scorecards_interview_worthy
    ON scorecards (interview_worthy, scored_at DESC);
"""


async def get_pool() -> asyncpg.Pool:
    settings = get_settings()
    return await asyncpg.create_pool(settings.database_url, min_size=1, max_size=5)


async def init_schema(pool: asyncpg.Pool | None = None) -> None:
    owns_pool = pool is None
    if pool is None:
        pool = await get_pool()
    try:
        async with pool.acquire() as conn:
            await conn.execute(SCHEMA_SQL)
    finally:
        if owns_pool:
            await pool.close()
