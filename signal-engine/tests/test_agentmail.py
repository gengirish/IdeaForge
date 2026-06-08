"""Tests for AgentMail digest email."""

from unittest.mock import MagicMock, patch

import pytest

from signal_engine.email.agentmail import send_email
from signal_engine.email.digest_mail import digest_subject, markdown_to_simple_html, send_digest_email
from signal_engine.config import Settings
from signal_engine.models import ThesisConfig


@pytest.mark.asyncio
async def test_send_email_no_api_key() -> None:
    settings = Settings(agentmail_api_key="", agentmail_digest_inbox_id="digest@test.com")
    result = await send_email(
        to="founder@example.com",
        subject="Hi",
        text="Body",
        settings=settings,
    )
    assert result.ok is False
    assert "AGENTMAIL_API_KEY" in result.reason


@pytest.mark.asyncio
async def test_send_email_success() -> None:
    mock_client = MagicMock()
    mock_response = MagicMock(message_id="msg_123")
    with patch("agentmail.AgentMail", return_value=mock_client):
        settings = Settings(
            agentmail_api_key="am_test",
            agentmail_digest_inbox_id="digest@intelliforge.tech",
        )
        result = await send_email(
            to="founder@example.com",
            subject="Digest",
            text="Plain",
            html="<p>HTML</p>",
            settings=settings,
        )
    assert result.ok is True
    mock_client.inboxes.messages.send.assert_called_once()


def test_markdown_to_simple_html_links() -> None:
    html_out = markdown_to_simple_html("See [signal](https://reddit.com/1)")
    assert '<a href="https://reddit.com/1">signal</a>' in html_out


def test_digest_subject() -> None:
    thesis = ThesisConfig(
        name="Recruiting TA",
        vertical="ta",
        icp={},
        problem_hypothesis="pain",
    )
    subject = digest_subject(thesis)
    assert "ThesisRadar" in subject
    assert "Recruiting TA" in subject


@pytest.mark.asyncio
async def test_send_digest_email_requires_recipient() -> None:
    thesis = ThesisConfig(
        name="Test",
        vertical="t",
        icp={},
        problem_hypothesis="p",
    )
    settings = Settings(
        agentmail_api_key="am_test",
        agentmail_digest_inbox_id="digest@test.com",
        digest_email_to="",
    )
    result = await send_digest_email(
        thesis=thesis,
        markdown_body="# Digest",
        settings=settings,
    )
    assert result.ok is False
    assert "DIGEST_EMAIL_TO" in result.reason
