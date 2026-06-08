"""Tests for LangSmith tracing configuration."""

import os

import signal_engine.tracing as tracing_module
from signal_engine.config import Settings
from signal_engine.tracing import configure_tracing


def test_configure_tracing_sets_env_when_enabled(monkeypatch) -> None:
    tracing_module._CONFIGURED = False
    monkeypatch.delenv("LANGCHAIN_TRACING_V2", raising=False)
    settings = Settings(
        langchain_tracing_v2=True,
        langchain_api_key="test-key",
        langchain_project="test-project",
    )
    assert configure_tracing(settings) is True
    assert os.environ["LANGCHAIN_TRACING_V2"] == "true"
    assert os.environ["LANGCHAIN_API_KEY"] == "test-key"
    assert os.environ["LANGCHAIN_PROJECT"] == "test-project"


def test_configure_tracing_disabled_without_key(monkeypatch) -> None:
    tracing_module._CONFIGURED = False
    monkeypatch.delenv("LANGCHAIN_TRACING_V2", raising=False)
    settings = Settings(langchain_tracing_v2=True, langchain_api_key="")
    assert configure_tracing(settings) is False
