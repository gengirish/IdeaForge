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
Tracing: LangSmith when LANGCHAIN_TRACING_V2=true
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

Output: `../docs/SIGNAL_DIGEST.md`

## Tests

```bash
uv run pytest
```

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
