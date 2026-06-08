"""Email delivery via AgentMail."""

from signal_engine.email.agentmail import SendResult, is_agentmail_enabled, send_email

__all__ = ["SendResult", "is_agentmail_enabled", "send_email"]
