"""LangSmith / LangChain tracing setup."""

from __future__ import annotations

import logging
import os

from signal_engine.config import Settings, get_settings

logger = logging.getLogger(__name__)

_CONFIGURED = False


def configure_tracing(settings: Settings | None = None) -> bool:
    """Enable LangSmith tracing when LANGCHAIN_TRACING_V2 and API key are set."""
    global _CONFIGURED
    if _CONFIGURED:
        return os.environ.get("LANGCHAIN_TRACING_V2") == "true"

    settings = settings or get_settings()
    if not settings.langchain_tracing_v2 or not settings.langchain_api_key:
        return False

    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
    os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project

    if settings.langchain_endpoint:
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint

    _CONFIGURED = True
    logger.info("LangSmith tracing enabled for project '%s'", settings.langchain_project)
    return True
