# ThesisRadar Signal Engine API (internal service)

FastAPI service wrapping `signal_engine` for ingestion and LLM scoring. Called **server-side only** by the Next.js fullstack app — not exposed to the browser.

## Run

```bash
cd apps/thesis-radar/api
uv sync
uv run uvicorn thesis_radar_api.main:app --reload --port 8000
```

Set `SIGNAL_ENGINE_API_URL=http://localhost:8000` in `apps/thesis-radar/web/.env.local`.

Open http://localhost:8000/docs for OpenAPI (dev only).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/v1/thesis/default` | Default thesis config |
| POST | `/v1/pipeline/dry-run` | Fetch signals without scoring |

The Next.js app exposes these at `/api/v1/*` and also calls them directly from Server Components via `@/lib/signal-engine`.
