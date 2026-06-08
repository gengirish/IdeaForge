# AgentMail — ThesisRadar / Signal Engine

Email integration for the **daily signal digest**. Source of truth: [docs.agentmail.to](https://docs.agentmail.to/) (not the outdated community skill at `open-source-skills/.../agentmail`).

## Pattern (from Vettd / IntelliForge)

| Item | Value |
|------|--------|
| Python SDK | `agentmail` package (`from agentmail import AgentMail`) |
| Reference impl | `interview-with-giri/backend/src/interviewbot/services/agentmail_client.py` |
| TS reference | `spinforge/spinforge/src/lib/email/agentmail.ts` |
| ADR | `ChairOS/docs/adr/0012-agentmail-for-email.md` |

## Environment

| Variable | Purpose |
|----------|---------|
| `AGENTMAIL_API_KEY` | API key from [console.agentmail.to](https://console.agentmail.to/) |
| `AGENTMAIL_DIGEST_INBOX_ID` | Sending inbox address (e.g. `digest@yourdomain.com`) — inbox id **is** the email |
| `DIGEST_EMAIL_TO` | Recipient for daily digest (dogfood: your email) |

Pre-create the inbox in the AgentMail console; do not rely on runtime inbox creation in production.

## Send flow

```
LangGraph: write_digest → send_digest_email
  → agentmail.inboxes.messages.send(inbox_id, {to, subject, text, html})
```

If `AGENTMAIL_API_KEY` or `DIGEST_EMAIL_TO` is unset, the node logs and skips (pipeline still succeeds).

## Webhook (Phase 1+)

Register inbound webhook for waitlist replies:

```text
POST https://thesis-radar.intelliforge.tech/api/webhooks/agentmail
```

HMAC verification per [webhook docs](https://docs.agentmail.to/).
