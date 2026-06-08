# ThesisRadar — Next.js Fullstack App

Next.js 14 App Router is the primary application surface for Phase 1. UI, API routes, Server Actions, auth, and billing all live here. The Python `signal-engine` runs as an internal service for ingestion and LLM scoring.

## Architecture

```
Browser
   │
   ▼
Next.js (Vercel)
   ├── Server Components  → direct server-side fetch
   ├── API Routes         → /api/v1/* (BFF for clients & webhooks)
   ├── Server Actions     → mutations (thesis wizard, billing — Phase 1)
   └── Postgres           → via DATABASE_URL (Prisma — Phase 1)
          │
          ▼
   Python signal-engine API (Fly.io / local :8000)
          └── LangGraph pipeline, LLM scoring, fetchers
```

## Run locally

**Terminal 1 — Python signal engine API:**

```bash
cd apps/thesis-radar/api
uv sync
uv run uvicorn thesis_radar_api.main:app --reload --port 8000
```

**Terminal 2 — Next.js fullstack app:**

```bash
cd apps/thesis-radar/web
cp .env.local.example .env.local
npm install
npm run dev
```

Open http://localhost:3000

## API routes (Next.js)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | App + signal-engine health |
| GET | `/api/v1/thesis/default` | Default thesis config |
| POST | `/api/v1/pipeline/dry-run` | Fetch signals without scoring |

Server Components can also import `@/lib/signal-engine` directly — no client round-trip needed.

## Environment

| Variable | Scope | Description |
|----------|-------|-------------|
| `SIGNAL_ENGINE_API_URL` | Server only | Python API base URL (default `http://localhost:8000`) |
| `DATABASE_URL` | Server only | Postgres for Prisma / Server Actions |
| `NEXT_PUBLIC_*` | Client | Only for browser-visible config (Clerk, etc.) |

## Phase 1 build list

- [ ] Thesis wizard (ICP, JTBD, competitors, keywords, disqualifiers)
- [ ] Daily email digest (Resend)
- [ ] Signal detail page with source receipts
- [ ] Scorecard view (5 dimensions)
- [ ] Auth + Stripe ($49/mo founding member)
- [ ] Waitlist landing page
- [ ] Prisma schema + Server Actions for thesis CRUD
