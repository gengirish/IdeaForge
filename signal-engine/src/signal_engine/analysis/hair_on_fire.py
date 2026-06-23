"""Aggregate hair-on-fire signals for reporting."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from signal_engine.models import ScoredSignal, ThesisConfig

HAIR_ON_FIRE_WINDOW_DAYS = 30


def filter_hair_on_fire(signals: list[ScoredSignal]) -> list[ScoredSignal]:
    """Return signals that meet the hair-on-fire rubric."""
    return [signal for signal in signals if signal.scorecard.hair_on_fire]


def render_hair_on_fire_analysis(
    thesis: ThesisConfig,
    signals: list[ScoredSignal],
    *,
    window_days: int = HAIR_ON_FIRE_WINDOW_DAYS,
    generated_at: datetime | None = None,
) -> str:
    now = generated_at or datetime.now(UTC)
    hair_on_fire = sorted(filter_hair_on_fire(signals), key=lambda s: -s.scorecard.urgency)

    lines = [
        "# Hair-on-Fire Analysis",
        "",
        f"> **Thesis:** {thesis.name}  ",
        f"> **Vertical:** {thesis.vertical}  ",
        f"> **Generated:** {now.strftime('%Y-%m-%d %H:%M UTC')}  ",
        f"> **Window:** last {window_days} days  ",
        f"> **Hair-on-fire signals:** {len(hair_on_fire)}",
        "",
        "Criteria: urgency ≥ 4, pain real, weekly frequency "
        "(see `docs/CUSTOMER_DISCOVERY_VALIDATION.md`).",
        "",
        "---",
        "",
    ]

    if not hair_on_fire:
        lines.extend(["_No hair-on-fire signals in this window yet._", ""])
        return "\n".join(lines)

    lines.extend(["## Signals", ""])
    for signal in hair_on_fire:
        scorecard = signal.scorecard
        lines.extend(
            [
                f"### [{signal.raw.title}]({signal.raw.url})",
                "",
                f"- **Urgency:** {scorecard.urgency}/5 | **Source:** {signal.raw.source.value}",
                f"- **Persona:** {scorecard.persona_fit.value} | "
                f"**Would pay:** {scorecard.would_pay.value}",
                f"- **Rationale:** {scorecard.rationale}",
                "",
            ]
        )

    return "\n".join(lines)


def write_hair_on_fire_analysis(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
