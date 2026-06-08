"""Markdown digest generation."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from signal_engine.analysis.contradictions import ContradictionAlert
from signal_engine.analysis.delta import DeltaSummary
from signal_engine.analysis.kill_criteria import KillCriteriaAlert
from signal_engine.models import ScoredSignal, ThesisConfig


def render_digest(
    thesis: ThesisConfig,
    scored_signals: list[ScoredSignal],
    *,
    delta: DeltaSummary | None = None,
    contradiction: ContradictionAlert | None = None,
    kill_criteria: list[KillCriteriaAlert] | None = None,
    generated_at: datetime | None = None,
) -> str:
    now = generated_at or datetime.now(UTC)
    interview_worthy = [s for s in scored_signals if s.scorecard.interview_worthy]
    other = [s for s in scored_signals if not s.scorecard.interview_worthy]

    lines = [
        "# Signal Digest",
        "",
        f"> **Thesis:** {thesis.name}  ",
        f"> **Generated:** {now.strftime('%Y-%m-%d %H:%M UTC')}  ",
        f"> **Signals scored:** {len(scored_signals)} | **Interview-worthy:** {len(interview_worthy)}",
        "",
        "---",
        "",
    ]

    if delta:
        lines.extend(_render_delta(delta))

    if contradiction and contradiction.count > 0:
        lines.extend(_render_contradictions(contradiction))

    if kill_criteria:
        lines.extend(_render_kill_criteria(kill_criteria))

    if interview_worthy:
        lines.extend(["## Interview-worthy signals", ""])
        for s in sorted(interview_worthy, key=lambda x: -x.scorecard.urgency):
            lines.extend(_format_signal(s, highlight=True))
    else:
        lines.extend(["## Interview-worthy signals", "", "_None today._", ""])

    lines.extend(["## Other signals", ""])
    if other:
        for s in sorted(other, key=lambda x: -x.scorecard.urgency)[:15]:
            lines.extend(_format_signal(s, highlight=False))
    else:
        lines.append("_None._")

    lines.extend(["", "---", "", "## Manual follow-up", ""])
    lines.extend(["### G2 competitor reviews", ""])
    for comp in thesis.competitors:
        name = comp.get("name", "Unknown")
        url = comp.get("g2_url", "")
        lines.append(f"- [{name}]({url})" if url else f"- {name}")

    lines.extend(["", "### LinkedIn search queries", ""])
    for q in thesis.linkedin_manual_queries[:10]:
        lines.append(f"- `{q}`")

    lines.append("")
    return "\n".join(lines)


def _render_delta(delta: DeltaSummary) -> list[str]:
    lines = [
        "## Since yesterday",
        "",
        f"- **New signals (24h):** {len(delta.new_since_prior_day)}",
        f"- **New interview-worthy:** {len(delta.new_interview_worthy)}",
        f"- **Total scored (24h):** {delta.total_last_24h}",
        f"- **Interview-worthy (24h):** {delta.interview_worthy_last_24h}",
        "",
    ]
    for s in delta.new_interview_worthy[:5]:
        lines.append(f"- 🔥 [{s.raw.title}]({s.raw.url})")
    if delta.new_interview_worthy:
        lines.append("")
    return lines


def _render_contradictions(alert: ContradictionAlert) -> list[str]:
    prefix = "⚠️ **ALERT:** " if alert.triggered else ""
    lines = [
        "## Contradiction alerts",
        "",
        f"{prefix}{alert.count} contradicting signal(s) in the last {alert.window_days} days "
        f"(threshold: {alert.threshold}).",
        "",
    ]
    if alert.message:
        lines.append(f"> {alert.message}")
        lines.append("")
    for s in alert.samples[:3]:
        lines.append(f"- [{s.raw.title}]({s.raw.url}) — _{s.scorecard.rationale}_")
    lines.append("")
    return lines


def _render_kill_criteria(alerts: list[KillCriteriaAlert]) -> list[str]:
    lines = ["## Kill criteria", ""]
    for alert in alerts:
        flag = "🛑 **TRIGGERED**" if alert.triggered else "✅ OK"
        lines.append(
            f"- {flag} **{alert.description}** — "
            f"{alert.current_value} vs threshold {alert.threshold} "
            f"({alert.window_days}d window) → _{alert.action}_"
        )
    lines.append("")
    return lines


def _format_signal(s: ScoredSignal, *, highlight: bool) -> list[str]:
    sc = s.scorecard
    flag = "🔥 " if highlight else ""
    block = [
        f"### {flag}[{s.raw.title}]({s.raw.url})",
        "",
        f"- **Source:** {s.raw.source.value} | **Urgency:** {sc.urgency}/5",
        f"- **Scorecard:** pain={sc.pain_real.value}, freq={sc.pain_frequency.value}, "
        f"expensive={sc.pain_expensive.value}, paying={sc.already_paying.value}, "
        f"persona={sc.persona_fit.value}, would_pay={sc.would_pay.value}, "
        f"thesis={sc.thesis_fit.value}",
        f"- **Rationale:** {sc.rationale}",
    ]
    if s.llm_provider:
        block.append(f"- **Scored by:** {s.llm_provider} ({s.llm_model})")
    block.append("")
    if sc.disqualifier_hit:
        block.insert(-1, f"- **Disqualifier hit:** {sc.disqualifier_hit}")
    return block


def write_digest(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
