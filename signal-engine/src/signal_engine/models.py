"""Domain models for thesis config, raw signals, and scorecards."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, computed_field


class PainFrequency(StrEnum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    RARE = "rare"


class PersonaFit(StrEnum):
    BUYER = "buyer"
    CHAMPION = "champion"
    USER_ONLY = "user-only"
    NOT_FIT = "not-fit"


class WouldPay(StrEnum):
    YES = "Y"
    MAYBE = "maybe"
    NO = "N"


class ThesisFit(StrEnum):
    SUPPORTS = "supports"
    NEUTRAL = "neutral"
    CONTRADICTS = "contradicts"


class YesNo(StrEnum):
    YES = "Y"
    NO = "N"


class SourceType(StrEnum):
    REDDIT = "reddit"
    HN = "hn"
    G2 = "g2"
    LINKEDIN = "linkedin"


class ThesisConfig(BaseModel):
    name: str
    vertical: str
    icp: dict
    problem_hypothesis: str
    keywords: list[str] = Field(default_factory=list)
    competitors: list[dict] = Field(default_factory=list)
    disqualifiers: list[str] = Field(default_factory=list)
    kill_criteria: list[dict] = Field(default_factory=list)
    sources: dict = Field(default_factory=dict)
    linkedin_manual_queries: list[str] = Field(default_factory=list)
    score_max_signals: int | None = None


class RawSignal(BaseModel):
    source: SourceType
    source_id: str
    url: str
    title: str
    body: str
    author: str = ""
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    content_hash: str = ""


class Scorecard(BaseModel):
    pain_real: YesNo
    pain_frequency: PainFrequency
    pain_expensive: YesNo
    already_paying: YesNo
    persona_fit: PersonaFit
    would_pay: WouldPay
    three_yes: YesNo
    thesis_fit: ThesisFit
    urgency: int = Field(ge=1, le=5)
    rationale: str = ""
    disqualifier_hit: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def hair_on_fire(self) -> bool:
        """18startup trait: buyer actively seeking relief (see docs/CUSTOMER_DISCOVERY_VALIDATION.md)."""
        if self.pain_real != YesNo.YES:
            return False
        if self.pain_frequency != PainFrequency.WEEKLY:
            return False
        return self.urgency >= 4

    @computed_field  # type: ignore[prop-decorator]
    @property
    def interview_worthy(self) -> bool:
        if self.disqualifier_hit:
            return False
        if self.pain_real != YesNo.YES:
            return False
        if self.persona_fit not in (PersonaFit.BUYER, PersonaFit.CHAMPION):
            return False
        if self.would_pay not in (WouldPay.YES, WouldPay.MAYBE):
            return False
        if self.urgency < 3:
            return False
        if self.pain_frequency == PainFrequency.RARE:
            return False
        return True


class ScoredSignal(BaseModel):
    raw: RawSignal
    scorecard: Scorecard
    thesis_name: str
    llm_provider: str | None = None
    llm_model: str | None = None


class FetchResult(BaseModel):
    signals: list[RawSignal]
    source: SourceType
