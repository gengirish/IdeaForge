"""Tests for LLM provider chain."""

from signal_engine.config import Settings
from signal_engine.llm.providers import build_provider_chain


def test_build_provider_chain_respects_order() -> None:
    settings = Settings(
        llm_provider_order="gemini,nvidia",
        gemini_api_key="gem-key",
        nvidia_nim_api_key="nv-key",
    )
    chain = build_provider_chain(settings)
    assert [p.name for p in chain] == ["Gemini", "NVIDIA NIM"]


def test_build_provider_chain_skips_missing_keys() -> None:
    settings = Settings(
        llm_provider_order="gemini,nvidia",
        nvidia_nim_api_key="nv-key",
    )
    chain = build_provider_chain(settings)
    assert len(chain) == 1
    assert chain[0].name == "NVIDIA NIM"
