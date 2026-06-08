# Build from repo root: fly deploy --config apps/thesis-radar/api/fly.toml
FROM python:3.12-slim-bookworm

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /usr/local/bin/uv

COPY signal-engine/ /app/signal-engine/
COPY apps/thesis-radar/api/ /app/apps/thesis-radar/api/

WORKDIR /app/apps/thesis-radar/api
RUN uv sync --frozen --no-dev

ENV SIGNAL_ENGINE_ROOT=/app
ENV DEFAULT_THESIS_PATH=/app/signal-engine/config/thesis_recruiting_ta.yaml
ENV PORT=8080

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "thesis_radar_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
