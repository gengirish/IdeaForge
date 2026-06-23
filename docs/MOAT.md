# Data moat — scheduled signal corpus

ThesisRadar’s defensibility is not the LLM scorer (commodity). It is the **proprietary, time-series evidence corpus** tied to explicit theses.

## What accumulates every 4 hours

| Layer | Where | Why it compounds |
|-------|--------|------------------|
| Raw + scored signals | Neon Postgres (`signals`, `scorecards`) | Upserted by `(source, source_id)` — corpus grows even when posts are re-seen |
| Run telemetry | `pipeline_runs` | Proof of continuous operation; ops + trend dashboards |
| Digest archive | `docs/digests/{vertical}/` | Human-readable audit trail per thesis per slot |
| Delta / contradictions / kill criteria | Digest + DB windows | Accuracy improves as 7d/14d history deepens |

## Schedule (GitHub Actions)

- **Cron:** `0 */4 * * *` — 6 runs/day at 00, 04, 08, 12, 16, 20 UTC
- **Thesis rotation:** `scripts/schedule_thesis.py` round-robins `config/thesis_*.yaml` by slot
- **Cost control:** prefilter cap (`score_max_signals` per thesis) + parallel scoring

## GitHub Actions vs Jenkins

| | GitHub Actions | Jenkins |
|---|----------------|---------|
| **This repo** | ✅ Already wired (secrets, cron, commit bot) | Would duplicate secrets + cron + checkout |
| **Ops** | Zero infra | Agent maintenance, plugins, creds rotation |
| **Moat** | Same Postgres either way | Same Postgres either way |

**Recommendation:** stay on GitHub Actions unless you need on-prem only. Jenkins can call the same CLI:

```bash
cd signal-engine
THESIS=$(uv run python scripts/schedule_thesis.py)
uv run python -m signal_engine.pipeline --thesis "$THESIS"
```

## Moat milestones

1. **Phase 0 (now):** 4h schedule + multi-thesis rotation + DB + archives
2. **Phase 1:** Dashboard reads Postgres — users see *your* historical delta, not a one-shot report
3. **Phase 2:** Export API / signed bundles for diligence; benchmark “interview-worthy precision” on labeled set
4. **Phase 3:** Fine-tune ranker on your scorecards; competitor can’t replicate without your labels + time depth

## Secrets required (GitHub)

`DATABASE_URL`, `NVIDIA_NIM_API_KEY`, `GEMINI_API_KEY`, `AGENTMAIL_*`, optional `LLM_SCORE_CONCURRENCY`, `LLM_SCORE_MAX_SIGNALS`
