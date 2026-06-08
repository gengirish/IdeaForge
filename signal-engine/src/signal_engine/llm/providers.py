"""OpenAI-compatible provider chain with retry + circuit breaker.

Ported from the ai-fallback-chain skill: cross-provider fallbacks, overload retries,
and circuit breaker on the primary provider.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass

from openai import AsyncOpenAI, APIStatusError, RateLimitError

from signal_engine.config import Settings, get_settings

logger = logging.getLogger(__name__)

FAILURE_THRESHOLD = 3
OPEN_DURATION_SEC = 300
MAX_RETRIES = 2
RETRY_BACKOFF_SEC = 1.5

# module-scoped circuit breaker (per serverless instance — acceptable for Phase 0)
_circuit: dict[str, tuple[int, float]] = {}


@dataclass(frozen=True)
class LLMProvider:
    name: str
    api_key: str
    base_url: str
    model: str


@dataclass(frozen=True)
class LLMProviderResult:
    content: str
    provider: str
    model: str


def _is_overload(exc: Exception) -> bool:
    if isinstance(exc, RateLimitError):
        return True
    if isinstance(exc, APIStatusError) and exc.status_code in (429, 503, 529):
        return True
    msg = str(exc).lower()
    return any(k in msg for k in ("overload", "rate limit", "capacity", "high demand"))


def _circuit_open(provider_name: str) -> bool:
    state = _circuit.get(provider_name)
    if not state:
        return False
    _, open_until = state
    return time.monotonic() < open_until


def _record_failure(provider_name: str) -> None:
    failures, _ = _circuit.get(provider_name, (0, 0.0))
    failures += 1
    open_until = 0.0
    if failures >= FAILURE_THRESHOLD:
        open_until = time.monotonic() + OPEN_DURATION_SEC
        logger.warning("Circuit open for %s (%ds)", provider_name, OPEN_DURATION_SEC)
    _circuit[provider_name] = (failures, open_until)


def _record_success(provider_name: str) -> None:
    _circuit[provider_name] = (0, 0.0)


def build_provider_chain(settings: Settings | None = None) -> list[LLMProvider]:
    settings = settings or get_settings()
    order = [p.strip() for p in settings.llm_provider_order.split(",") if p.strip()]
    providers: list[LLMProvider] = []

    catalog = {
        "nvidia": lambda: LLMProvider(
            name="NVIDIA NIM",
            api_key=settings.nvidia_nim_api_key,
            base_url=settings.nvidia_nim_base_url,
            model=settings.nvidia_nim_model,
        ),
        "gemini": lambda: LLMProvider(
            name="Gemini",
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url,
            model=settings.gemini_model,
        ),
    }

    for key in order:
        factory = catalog.get(key)
        if not factory:
            continue
        provider = factory()
        if provider.api_key:
            providers.append(provider)

    return providers


async def _call_once(provider: LLMProvider, prompt: str) -> str:
    client = AsyncOpenAI(api_key=provider.api_key, base_url=provider.base_url)
    response = await client.chat.completions.create(
        model=provider.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError(f"Empty response from {provider.name}")
    return content


async def call_llm_json(
    prompt: str,
    *,
    settings: Settings | None = None,
) -> LLMProviderResult:
    """Call LLM providers in order until one succeeds."""
    settings = settings or get_settings()
    providers = build_provider_chain(settings)
    if not providers:
        raise RuntimeError(
            "No LLM providers configured. Set NVIDIA_NIM_API_KEY and/or GEMINI_API_KEY."
        )

    last_error: Exception | None = None
    for i, provider in enumerate(providers):
        if i == 0 and _circuit_open(provider.name):
            logger.info("Skipping %s (circuit open)", provider.name)
            continue

        for attempt in range(MAX_RETRIES):
            try:
                content = await _call_once(provider, prompt)
                _record_success(provider.name)
                return LLMProviderResult(
                    content=content,
                    provider=provider.name,
                    model=provider.model,
                )
            except Exception as exc:
                last_error = exc
                if i == 0:
                    _record_failure(provider.name)
                if _is_overload(exc) and attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_BACKOFF_SEC * (attempt + 1))
                    continue
                logger.warning("%s failed: %s", provider.name, exc)
                break

    raise RuntimeError(f"All LLM providers failed: {last_error}") from last_error
