# IdeaForge (Signal Engine / ThesisRadar)

Thesis-driven, evidence-grade daily signal engine for founders with an active bet.

> *Is my problem hair-on-fire for this specific buyer — and who do I talk to next?*

See [IDEA_DISCOVERY_ENGINE_ROADMAP.md](./IDEA_DISCOVERY_ENGINE_ROADMAP.md) for the full product roadmap.

## Monorepo layout

```
IdeaForge/
├── signal-engine/          # Phase 0 CLI — ingestion, scoring, digest
├── apps/thesis-radar/      # Phase 1 web product (scaffold)
│   ├── api/                # FastAPI wrapper over signal_engine
│   └── web/                # Next.js dashboard
└── docs/                   # Discovery tracker, digests, analysis
```

## Quick start — Phase 0

```bash
docker compose up -d   # Postgres (matches .env.example DATABASE_URL)
cp .env.example .env   # fill LLM keys

# From repo root (recommended):
npm run pipeline:dry-run   # fetch only
npm run pipeline           # full run → docs/SIGNAL_DIGEST.md

# Or from signal-engine/:
cd signal-engine
uv sync --group test
uv run python -m signal_engine.pipeline --dry-run
uv run python -m signal_engine.pipeline
uv run pytest -q
```

**Agent workflow:** See [AGENTS.md](./AGENTS.md) and [implementation plan](./docs/superpowers/plans/2026-06-07-ideaforge-complete-product-plan.md) — skills are mandatory per phase.

## Phase 1 (Next.js fullstack)

Run everything from the **repo root** (`IdeaForge/`):

```bash
# Python signal-engine service (ingestion + scoring)
cd apps/thesis-radar/api && uv sync && uv run uvicorn thesis_radar_api.main:app --reload --port 8000

# Next.js fullstack app (UI + API routes + Server Actions)
cp apps/thesis-radar/web/.env.local.example apps/thesis-radar/web/.env.local
npm install --prefix apps/thesis-radar/web
npm run dev
```

## Stack

| Layer | Tech |
|-------|------|
| App (fullstack) | Next.js 14 App Router — Server Components, API routes, Server Actions |
| Signal engine | Python 3.12, uv, httpx, asyncpg, Pydantic (internal service) |
| Scoring | LangGraph nodes + NVIDIA NIM → Gemini fallback (circuit breaker) |
| Storage | Postgres |
| Auth / billing (Phase 1) | Clerk + Stripe via Next.js |
| Deploy | Vercel → [thesis-radar.intelliforge.tech](https://thesis-radar.intelliforge.tech) · Fly → thesis-radar-api.fly.dev |
| CI | GitHub Actions (daily digest cron) |
