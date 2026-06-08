"""Delta view — what's new since yesterday."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, Field

from signal_engine.models import ScoredSignal


class DeltaSummary(BaseModel):
    since: datetime
    new_since_prior_day: list[ScoredSignal] = Field(default_factory=list)
    new_interview_worthy: list[ScoredSignal] = Field(default_factory=list)
    total_last_24h: int = 0
    interview_worthy_last_24h: int = 0


def compute_delta(
    *,
    last_24h: list[ScoredSignal],
    prior_24h: list[ScoredSignal],
    now: datetime | None = None,
) -> DeltaSummary:
    """Signals in the last 24h that weren't present in the prior 24h window."""
    now = now or datetime.now(UTC)
    since = now - timedelta(hours=24)
    prior_keys = {(s.raw.source, s.raw.source_id) for s in prior_24h}

    new_since_prior_day = [
        s for s in last_24h if (s.raw.source, s.raw.source_id) not in prior_keys
    ]
    new_interview_worthy = [s for s in new_since_prior_day if s.scorecard.interview_worthy]

    return DeltaSummary(
        since=since,
        new_since_prior_day=new_since_prior_day,
        new_interview_worthy=new_interview_worthy,
        total_last_24h=len(last_24h),
        interview_worthy_last_24h=sum(1 for s in last_24h if s.scorecard.interview_worthy),
    )
