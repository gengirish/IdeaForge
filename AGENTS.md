# IdeaForge — Agent Instructions

This repo builds **ThesisRadar** (Signal Engine). Before writing code, **read and follow the skills listed for your phase** (see `docs/superpowers/plans/2026-06-07-ideaforge-complete-product-plan.md`).

## EU launch (Romanian SRL — shared with ComplianceForge)

Portfolio launch is **paused** but documented. When resuming:

1. **Resume here:** [`docs/EU_LAUNCH_STATUS.md`](./docs/EU_LAUNCH_STATUS.md)
2. **Full plan:** [`docs/EU_LAUNCH_PLAN.md`](./docs/EU_LAUNCH_PLAN.md)
3. **Order:** ComplianceForge first (`D:\codebase\complianceforge`) → ThesisRadar second

## Non-negotiable workflow

1. **Identify phase** from `IDEA_DISCOVERY_ENGINE_ROADMAP.md`
2. **Invoke applicable skills** (Read skill file) before implementation
3. **Write/adjust tests** (`test-driven-development`, `writing-tests`)
4. **Run verification** (`verification-before-completion`) before claiming done

## Skill map by phase

| Phase | Goal | Required skills |
|-------|------|-----------------|
| **0** | Daily digest dogfood | `langchain-architecture`, `ai-fallback-chain`, `ws-python-development`, `ws-database-design`, `adding-docker`, `setting-up-ci`, `verification-before-completion` |
| **1** | 10 paying beta users | `tk-nextjs`, `tk-shadcn-ui`, `tk-fastapi`, `adding-auth`, `adding-stripe`, `prod-landing-page`, `mkt-copywriting`, **AgentMail** (`docs/AGENTMAIL.md`) |
| **2** | Retention / thesis monitoring | `langchain-architecture` (checkpointing), `ws-llm-application-dev`, `ws-observability` |
| **3** | Acquisition | `mkt-seo-audit`, `prod-landing-page`, `adding-feature-flags` |
| **4** | Moat | `ws-database-design`, `adding-api-docs`, `ws-signed-audit-trails` |

## Production domains

| Surface | URL |
|---------|-----|
| **Web (primary)** | https://thesis-radar.intelliforge.tech |
| API | https://thesis-radar-api.fly.dev |

Vercel hosts the Next.js app; Fly hosts the Python API. Never ship this UI on vettd-app.com.

## Repo layout

```
signal-engine/           # LangGraph pipeline, scoring, digest (Phase 0–2)
apps/thesis-radar/
  api/                   # FastAPI (Phase 1)
  web/                   # Next.js (Phase 1)
docs/                    # Tracker, digests, plans
```

## Commands

All commands assume **repo root** (`IdeaForge/`):

```bash
docker compose up -d          # Postgres for local pipeline
npm run pipeline              # full digest (from repo root)
npm run pipeline:dry-run      # fetch only
cd signal-engine && uv run pytest -q
npm run build                 # Next.js (apps/thesis-radar/web)
npm run dev                   # Next.js dev server
npm run deploy:api            # Fly.io
npm run deploy:web            # Vercel
```

## What NOT to do

- Do not scaffold features without the matching skill
- Do not claim Phase 1 complete without auth + Stripe + AgentMail (roadmap P0)
- Do not ship Signal Engine UI on vettd-app.com (separate brand)
