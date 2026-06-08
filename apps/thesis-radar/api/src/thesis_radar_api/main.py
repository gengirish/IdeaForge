"""FastAPI application."""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from signal_engine.models import RawSignal
from signal_engine.graph.nodes import load_thesis
from signal_engine.pipeline import fetch_all


def _default_thesis_path() -> Path:
    if path := os.getenv("DEFAULT_THESIS_PATH"):
        return Path(path)
    if root := os.getenv("SIGNAL_ENGINE_ROOT"):
        return Path(root) / "signal-engine" / "config" / "thesis_recruiting_ta.yaml"
    return (
        Path(__file__).resolve().parents[5] / "signal-engine" / "config" / "thesis_recruiting_ta.yaml"
    )


DEFAULT_THESIS = _default_thesis_path()


def _cors_origins() -> list[str]:
    raw = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,https://thesis-radar.intelliforge.tech,https://thesis-radar.vercel.app",
    )
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="ThesisRadar API",
    description="Thesis-driven signal engine API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    version: str


class SignalSummary(BaseModel):
    source: str
    title: str
    url: str


class DryRunResponse(BaseModel):
    count: int
    signals: list[SignalSummary]


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    from thesis_radar_api import __version__

    return HealthResponse(status="ok", version=__version__)


@app.get("/v1/thesis/default")
async def get_default_thesis() -> dict:
    if not DEFAULT_THESIS.exists():
        raise HTTPException(status_code=404, detail="Default thesis config not found")
    return yaml.safe_load(DEFAULT_THESIS.read_text(encoding="utf-8"))


@app.post("/v1/pipeline/dry-run", response_model=DryRunResponse)
async def pipeline_dry_run() -> DryRunResponse:
    thesis = load_thesis(DEFAULT_THESIS)
    signals: list[RawSignal] = await fetch_all(thesis)
    return DryRunResponse(
        count=len(signals),
        signals=[
            SignalSummary(source=s.source.value, title=s.title, url=s.url) for s in signals[:50]
        ],
    )
