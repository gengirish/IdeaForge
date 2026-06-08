# IdeaForge Complete Product Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` or `subagent-driven-development` task-by-task. Check boxes as you go.

**Goal:** Ship ThesisRadar from Phase 0 dogfood through Phase 1 MVP using the identified Cursor skills — not ad-hoc scaffolding.

**Architecture:** LangGraph orchestrates ingestion → scoring → retention analysis → digest. FastAPI wraps `signal_engine` for the web. Next.js + Clerk + Stripe + Resend for Phase 1.

**Tech Stack:** Python 3.12, uv, LangGraph, asyncpg, FastAPI, Next.js 14, shadcn, Clerk, Stripe, Resend, Neon Postgres

---

## Status snapshot (2026-06-07)

| Area | Built | Skill used? | Gap |
|------|-------|-------------|-----|
| LangGraph pipeline | ✅ | Partial | Interview pack export node missing |
| LLM fallback chain | ✅ | Partial | No probe script from `ai-fallback-chain` |
| Phase 2 analysis | ✅ | Partial | No LangGraph checkpointer yet |
| LangSmith tracing | ✅ | Partial | Optional env only |
| Postgres | ✅ schema | ❌ | No Docker local dev until now |
| CI tests | ❌ | ❌ | Only digest cron workflow |
| Thesis wizard | ❌ | ❌ | Phase 1 |
| Auth + Stripe | ❌ | ❌ | Phase 1 |
| Resend digest | ❌ | ❌ | Phase 1 |
| Waitlist landing | Scaffold | ❌ | Needs `prod-landing-page` |

---

## Phase 0 — finish dogfood loop

**Skills:** `adding-docker`, `setting-up-ci`, `verification-before-completion`, `ai-fallback-chain`

- [x] Task 0.1: `docker-compose.yml` for local Postgres
- [x] Task 0.2: `.github/workflows/ci.yml` — pytest + web build
- [x] Task 0.3: `.cursor/rules/` skill gates + `AGENTS.md`
- [ ] Task 0.4: Run full pipeline against Docker Postgres with LLM keys
- [ ] Task 0.5: 3 weeks digest validation (human — roadmap exit criteria)
- [ ] Task 0.6: Add LLM model probe script (`ai-fallback-chain` reference)

---

## Phase 1 — MVP (after Phase 0 exit)

**Skills:** `tk-nextjs`, `tk-shadcn-ui`, `tk-fastapi`, `adding-auth`, `adding-stripe`, `prod-landing-page`, `mkt-copywriting`

### Task 1.1: Waitlist landing (`prod-landing-page`, `mkt-copywriting`)

- [ ] Hero: thesis-driven positioning (not idea tourist)
- [ ] Waitlist form → API route → DB or Resend audience
- [ ] Founding member $49/mo CTA copy

### Task 1.2: Thesis wizard (`tk-react-hook-form`, `tk-zod`)

- [ ] Multi-step: ICP, JTBD, keywords, competitors, disqualifiers, kill criteria
- [ ] Export/import YAML compatible with `signal-engine/config/`

### Task 1.3: Auth (`adding-auth` or `tk-clerk`)

- [ ] Clerk separate from Vettd
- [ ] Protect dashboard routes

### Task 1.4: Stripe (`adding-stripe`, `ws-payment-processing`)

- [ ] $49/mo founding member price
- [ ] 20-seat cap webhook logic
- [ ] Customer portal link in settings

### Task 1.5: Resend daily digest

- [ ] Email template mirroring markdown digest sections
- [ ] Cron or queue trigger post-pipeline

### Task 1.6: Signal detail + scorecard UI (`tk-shadcn-ui`)

- [ ] Source receipt links (no black-box scores)
- [ ] 5-dimension scorecard view

---

## Phase 2 — retention

**Skills:** `langchain-architecture`, `ws-observability`

- [x] Delta view, contradiction alerts, kill criteria in digest
- [ ] Interview pack export node
- [ ] Postgres LangGraph checkpointer for post-interview re-score
- [ ] Slack digest integration

---

## Verification checklist (every PR)

- [ ] `cd signal-engine && uv run pytest -q` — 0 failures
- [ ] `cd apps/thesis-radar/web && npm run build` — exit 0
- [ ] Skills used are listed in PR description
