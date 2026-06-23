# Signal Engine (Phase 0)

Daily evidence pipeline orchestrated with **LangGraph**: fetch Reddit/HN → dedupe → score → store → digest.

## Architecture

```
LangGraph StateGraph
  load_thesis → fetch_sources → dedupe
    ├─ (dry-run) → render_digest → write_digest
    └─ score_batch → persist → analyze_retention → render_digest → write_digest

analyze_retention: delta view, contradiction alerts, kill criteria (Phase 2)
LLM scoring: ai-fallback-chain (NVIDIA NIM → Gemini, circuit breaker)
Parallel scoring: `LLM_SCORE_CONCURRENCY` (default 8) — asyncio batch with aggregated errors
Pre-LLM cap: `LLM_SCORE_MAX_SIGNALS` (default 50) or per-thesis `score_max_signals` — keyword rank then top-N

## Thesis configs

| File | Vertical |
|------|----------|
| `config/thesis_recruiting_ta.yaml` | Recruiting / TA (Vettd dogfood) |
| `config/thesis_soc2_compliance.yaml` | SOC 2 / compliance for B2B startups |

```bash
npm run pipeline:soc2:dry-run   # SOC 2 topic, fetch only
npm run pipeline:soc2           # SOC 2 topic, full run
```
Tracing: LangSmith when LANGCHAIN_TRACING_V2=true
Email: AgentMail send_digest_email node (see ../docs/AGENTMAIL.md)
```

## Setup

```bash
uv sync --group test
cp ../.env.example ../.env
# Set DATABASE_URL, NVIDIA_NIM_API_KEY or GEMINI_API_KEY
```

## Database

Apply schema on first run (or manually):

```bash
uv run python -c "import asyncio; from signal_engine.db import init_schema; asyncio.run(init_schema())"
```

## Run

```bash
uv run python -m signal_engine.pipeline --dry-run   # fetch only, no LLM/DB
uv run python -m signal_engine.pipeline             # full pipeline
uv run python -m signal_engine.pipeline --thesis config/thesis_recruiting_ta.yaml
```

Output: `../docs/SIGNAL_DIGEST.md` + `../docs/digests/{vertical}/`

## Scheduled runs (moat)

GitHub Actions runs the pipeline **every 4 hours** with thesis rotation. See [docs/MOAT.md](../docs/MOAT.md).

```bash
uv run python scripts/schedule_thesis.py   # which thesis runs this slot?
```

## Tuning sources

Edit `config/thesis_recruiting_ta.yaml`:

| Reddit | HN |
|--------|-----|
| `keywords:` — one PullPush query per term (no `OR` chains) | `days_back: 30` — default window |
| `days_back: 14` — local recency filter (relaxed if PullPush index lags) | `days_back: 30` — Algolia time window |
| `fallback_listing: true` — list + local keyword filter if empty | `query:` — each word queried separately |

Probe hit counts: `uv run python scripts/probe_sources.py`

## Config

Thesis YAML lives in `config/`. See `thesis_recruiting_ta.yaml` for the Vettd dogfood vertical.

## Scoring rubric

| Field | Values |
|-------|--------|
| Pain real? | Y / N |
| Pain frequent? | weekly / monthly / rare |
| Pain expensive? | Y / N |
| Already paying? | Y / N |
| Persona fit | buyer / champion / user-only / not-fit |
| Would pay? | Y / maybe / N |
| 3-yes signal | Y / N |
| Thesis fit | supports / neutral / contradicts |
| Urgency | 1–5 |

**Interview-worthy gate:** pain real + buyer/champion + would pay ∈ {Y, maybe} + urgency ≥ 3 + frequency ≥ monthly + no disqualifier hit.
