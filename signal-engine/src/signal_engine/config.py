"""Application settings from environment."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql://ideaforge:ideaforge@localhost:5432/ideaforge"

    # Comma-separated provider order (cross-provider fallbacks — ai-fallback-chain)
    llm_provider_order: str = "nvidia,gemini"

    nvidia_nim_api_key: str = ""
    nvidia_nim_base_url: str = "https://integrate.api.nvidia.com/v1"
    # Llama-4-Maverick: ~4s latency, valid JSON (ai-fallback-chain probe results)
    nvidia_nim_model: str = "meta/llama-4-maverick-17b-128e-instruct"

    gemini_api_key: str = ""
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    gemini_model: str = "gemini-2.0-flash"

    digest_output_path: str = "../docs/SIGNAL_DIGEST.md"

    # LangSmith observability (langchain-architecture)
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "thesis-radar"
    langchain_endpoint: str = ""

    # AgentMail — daily digest (docs/AGENTMAIL.md)
    agentmail_api_key: str = ""
    agentmail_digest_inbox_id: str = ""
    digest_email_to: str = ""


def get_settings() -> Settings:
    return Settings()
