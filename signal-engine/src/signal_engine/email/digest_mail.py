"""Format and send the daily signal digest via AgentMail."""

from __future__ import annotations

import html
import re
from datetime import UTC, datetime

from signal_engine.config import Settings, get_settings
from signal_engine.email.agentmail import SendResult, send_email
from signal_engine.models import ThesisConfig


def markdown_to_simple_html(md: str) -> str:
    """Minimal markdown → HTML for email clients."""
    escaped = html.escape(md)
    # Links: [text](url)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        escaped,
    )
    # Bold from **text**
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    lines = escaped.split("\n")
    body = "<br>\n".join(lines)
    return f"""<!DOCTYPE html>
<html><body style="font-family: system-ui, sans-serif; line-height: 1.5; color: #111;">
{body}
<hr>
<p style="color:#666;font-size:12px;">ThesisRadar daily signal digest</p>
</body></html>"""


def digest_subject(thesis: ThesisConfig, *, now: datetime | None = None) -> str:
    day = (now or datetime.now(UTC)).strftime("%Y-%m-%d")
    return f"ThesisRadar — {thesis.name} — {day}"


async def send_digest_email(
    *,
    thesis: ThesisConfig,
    markdown_body: str,
    settings: Settings | None = None,
) -> SendResult:
    settings = settings or get_settings()
    recipient = settings.digest_email_to
    if not recipient:
        return SendResult(ok=False, reason="DIGEST_EMAIL_TO not set")

    subject = digest_subject(thesis)
    html_body = markdown_to_simple_html(markdown_body)
    return await send_email(
        to=recipient,
        subject=subject,
        text=markdown_body,
        html=html_body,
        settings=settings,
    )
