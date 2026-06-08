"""LLM-based signal scoring via resilient provider chain."""

from __future__ import annotations

import json
import logging

from signal_engine.config import Settings, get_settings
from signal_engine.llm.providers import call_llm_json
from signal_engine.models import (
    PainFrequency,
    PersonaFit,
    RawSignal,
    Scorecard,
    ScoredSignal,
    ThesisConfig,
    ThesisFit,
    WouldPay,
    YesNo,
)

logger = logging.getLogger(__name__)

SCORE_PROMPT = """You are a customer discovery analyst scoring evidence against a founder's thesis.

## Thesis
Name: {thesis_name}
ICP: {icp}
Problem hypothesis: {problem_hypothesis}
Disqualifiers (if any match, set disqualifier_hit to the matched phrase):
{disqualifiers}

## Signal
Source: {source}
Title: {title}
Body: {body}

Score this signal. Return ONLY valid JSON with these exact keys:
{{
  "pain_real": "Y" or "N",
  "pain_frequency": "weekly" or "monthly" or "rare",
  "pain_expensive": "Y" or "N",
  "already_paying": "Y" or "N",
  "persona_fit": "buyer" or "champion" or "user-only" or "not-fit",
  "would_pay": "Y" or "maybe" or "N",
  "three_yes": "Y" or "N",
  "thesis_fit": "supports" or "neutral" or "contradicts",
  "urgency": 1-5 integer,
  "rationale": "one sentence citing specific evidence from the signal",
  "disqualifier_hit": null or "matched disqualifier phrase"
}}

Rules:
- pain_real=Y only if a specific past instance is described, not vague annoyance
- three_yes=Y only if pain_real=Y AND persona_fit in (buyer,champion) AND would_pay in (Y,maybe)
- urgency 5 = hair-on-fire, 1 = mild curiosity
"""


def _parse_scorecard(raw: dict) -> Scorecard:
    return Scorecard(
        pain_real=YesNo(raw["pain_real"]),
        pain_frequency=PainFrequency(raw["pain_frequency"]),
        pain_expensive=YesNo(raw["pain_expensive"]),
        already_paying=YesNo(raw["already_paying"]),
        persona_fit=PersonaFit(raw["persona_fit"]),
        would_pay=WouldPay(raw["would_pay"]),
        three_yes=YesNo(raw["three_yes"]),
        thesis_fit=ThesisFit(raw["thesis_fit"]),
        urgency=int(raw["urgency"]),
        rationale=str(raw.get("rationale", "")),
        disqualifier_hit=raw.get("disqualifier_hit"),
    )


async def score_signal(
    signal: RawSignal,
    thesis: ThesisConfig,
    *,
    settings: Settings | None = None,
) -> ScoredSignal:
    settings = settings or get_settings()
    prompt = SCORE_PROMPT.format(
        thesis_name=thesis.name,
        icp=json.dumps(thesis.icp),
        problem_hypothesis=thesis.problem_hypothesis.strip(),
        disqualifiers="\n".join(f"- {d}" for d in thesis.disqualifiers) or "(none)",
        source=signal.source.value,
        title=signal.title,
        body=signal.body[:4000],
    )

    result = await call_llm_json(prompt, settings=settings)
    parsed = json.loads(result.content)
    scorecard = _parse_scorecard(parsed)
    logger.debug("Scored via %s (%s)", result.provider, result.model)

    return ScoredSignal(
        raw=signal,
        scorecard=scorecard,
        thesis_name=thesis.name,
        llm_provider=result.provider,
        llm_model=result.model,
    )
