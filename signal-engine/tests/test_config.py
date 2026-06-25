"""Tests for application settings."""

import os

from signal_engine.config import Settings


def test_empty_env_int_vars_use_defaults(monkeypatch) -> None:
    """Unset optional int env vars (empty string) fall back to defaults."""
    monkeypatch.setenv("LLM_SCORE_CONCURRENCY", "")
    monkeypatch.setenv("LLM_SCORE_MAX_SIGNALS", "")

    settings = Settings()

    assert settings.llm_score_concurrency == 8
    assert settings.llm_score_max_signals == 50


def test_env_int_vars_override_defaults(monkeypatch) -> None:
    monkeypatch.setenv("LLM_SCORE_CONCURRENCY", "4")
    monkeypatch.setenv("LLM_SCORE_MAX_SIGNALS", "25")

    settings = Settings()

    assert settings.llm_score_concurrency == 4
    assert settings.llm_score_max_signals == 25
