"""AgentMail client — pattern from interview-with-giri agentmail_client.py.

Official API: https://docs.agentmail.to/ (api.agentmail.to)
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from signal_engine.config import Settings, get_settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SendResult:
    ok: bool
    reason: str = ""
    message_id: str | None = None


def is_agentmail_enabled(settings: Settings | None = None) -> bool:
    settings = settings or get_settings()
    return bool(settings.agentmail_api_key and settings.agentmail_digest_inbox_id)


def _get_client(settings: Settings) -> Any | None:
    if not settings.agentmail_api_key:
        return None
    from agentmail import AgentMail

    return AgentMail(api_key=settings.agentmail_api_key)


async def send_email(
    *,
    to: str,
    subject: str,
    text: str,
    html: str | None = None,
    inbox_id: str | None = None,
    settings: Settings | None = None,
) -> SendResult:
    """Send from the digest inbox. No-op-safe when not configured."""
    settings = settings or get_settings()
    resolved_inbox = inbox_id or settings.agentmail_digest_inbox_id

    if not settings.agentmail_api_key:
        return SendResult(ok=False, reason="AGENTMAIL_API_KEY not set")
    if not resolved_inbox:
        return SendResult(ok=False, reason="AGENTMAIL_DIGEST_INBOX_ID not set")
    if not to:
        return SendResult(ok=False, reason="recipient empty")

    client = _get_client(settings)
    if client is None:
        return SendResult(ok=False, reason="client unavailable")

    try:
        kwargs: dict[str, Any] = {"to": to, "subject": subject, "text": text}
        if html:
            kwargs["html"] = html
        response = await asyncio.to_thread(
            client.inboxes.messages.send,
            resolved_inbox,
            **kwargs,
        )
        message_id = getattr(response, "message_id", None) or getattr(response, "messageId", None)
        logger.info("agentmail_sent to=%s subject=%s", to, subject)
        return SendResult(ok=True, message_id=str(message_id) if message_id else None)
    except Exception as exc:
        logger.error("agentmail_send_failed to=%s error=%s", to, exc)
        return SendResult(ok=False, reason=str(exc))
