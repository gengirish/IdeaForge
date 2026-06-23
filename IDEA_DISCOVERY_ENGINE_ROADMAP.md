# Idea Discovery Engine — Product Roadmap

> **Working name:** Signal Engine / ThesisRadar  
> **Status:** Phase 0 shipped (dogfood). Phases 1–4 are the path to a standalone MVP.  
> **Build mode:** Parallel to Vettd — same repo, separate product surface (`signal-engine/`).

---

## What this product is

Not another “validate any startup idea in 10 seconds” tool. This is a **thesis-driven, evidence-grade, daily signal engine** that answers:

> *Is my problem hair-on-fire for this specific buyer — and who do I talk to next?*

**Positioning:** Daily evidence for founders who already have a bet — not idea tourists browsing random niches.

**Wedge vs. PainHunt / GapFinder / Trendstr:**

| They optimize for | We optimize for |
|-------------------|-----------------|
| Broad niche → idea suggestions | Your ICP + JTBD thesis → urgency evidence |
| Single 0–100 score | Scorecard: pain real, frequency, expensive, paying, would pay |
| One-time validation report | Daily delta + contradiction alerts |
| Idea generation | Signal → interview target → outreach angle |

---

## Relationship to Vettd

| | Vettd | Idea Discovery Engine |
|---|-------|----------------------|
| **Buyer** | Recruiters / TA leads | Founders, scouts, PMs with an active thesis |
| **Job** | Run AI interviews | Find and score hair-on-fire problems |
| **Phase 0 vertical** | Recruiting/TA (dogfood) | Same — proves the loop on real discovery work |
| **Code location** | `backend/`, `frontend/` | `signal-engine/` (standalone package today) |
| **Brand** | vettd-app.com | Separate brand at Phase 1 (e.g. ThesisRadar) |

**Strategy:** Dogfood on Vettd’s recruiting thesis first. If Phase 0 hits the success metric, productize horizontally without confusing Vettd’s recruiter positioning.

---

## Architecture (target end state)

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   Sources   │────▶│  Ingestion   │────▶│   Scoring   │────▶│   Actions    │
│ Reddit/HN   │     │ dedupe+store │     │ evidence    │     │ digest/email │
│ G2/reviews  │     │ Postgres     │     │ NVIDIA/Gemini│     │ outreach     │
│ LinkedIn*   │     │              │     │ scorecard   │     │ interview Qs │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                           │                    │
                           └────────┬───────────┘
                                    ▼
                           Thesis YAML (ICP, disqualifiers,
                           problem hypothesis, kill criteria)
```

\* LinkedIn automated in Phase 2+; manual queries in Phase 0.

**Scoring rubric** (ported from `docs/CUSTOMER_DISCOVERY_TRACKER.md`):

| Field | Values | Meaning |
|-------|--------|---------|
| Pain real? | Y / N | Specific past instance, not vague annoyance |
| Pain frequent? | weekly / monthly / rare | |
| Pain expensive? | Y / N | Quantified cost (hours, money, lost deals) |
| Already paying? | Y / N | Workaround spend = strongest PMF signal |
| Persona fit | buyer / champion / user-only / not-fit | |
| Would pay? | Y / maybe / N | |
| 3-yes signal | Y / N | Pain real + buyer/champion + would pay |
| Thesis fit | supports / neutral / contradicts | Strengthens or kills your hypothesis |
| Urgency | 1–5 | Composite hair-on-fire score |

**Interview-worthy gate:** pain real + buyer/champion + would pay ∈ {Y, maybe} + urgency ≥ 3 + frequency ≥ monthly + no disqualifier hit.

---

## Phase overview

| Phase | Timeline | Goal | Ship to |
|-------|----------|------|---------|
| **0** | 2–3 weeks | Prove the loop on yourself | Markdown digest |
| **1** | 4–6 weeks | 10 paying beta users | Web app MVP |
| **2** | 6–8 weeks | Retention (daily habit) | Thesis monitoring |
| **3** | 8–12 weeks | Repeatable acquisition | Vertical packs + SEO |
| **4** | Month 6+ | Moat | Outcome database + API |

---

## Phase 0 — Prove the loop (dogfood)

**Goal:** One vertical (recruiting/TA), one daily digest you’d actually read.

**Status:** ✅ **Shipped** in `signal-engine/`

### Deliverables

| Item | Status | Location |
|------|--------|----------|
| Thesis config (ICP + disqualifiers) | ✅ | `signal-engine/config/thesis_recruiting_ta.yaml` |
| Reddit ingestion (PullPush + listing) | ✅ | `fetchers/reddit.py` |
| HN ingestion (Algolia) | ✅ | `fetchers/hn.py` |
| G2 competitor links | 📋 manual | In digest footer |
| LinkedIn search queries (10) | 📋 manual | In digest footer |
| Scoring rubric automation | ✅ | `scorer.py` (NVIDIA NIM → Gemini fallback) |
| Postgres storage | ✅ | `db.py`, `repository.py` |
| Daily markdown digest | ✅ | `docs/SIGNAL_DIGEST.md` |
| GitHub Action cron | ✅ | `.github/workflows/signal-digest.yml` |
| Tests | ✅ | `signal-engine/tests/` |

### Success metric

**≥1 interview-worthy signal per week** you wouldn’t have found manually.

### Stack

Python 3.12 · uv · httpx · asyncpg · OpenAI-compatible LLM (NVIDIA NIM / Gemini) · Postgres · GitHub Actions

### Run locally

```bash
cd signal-engine
uv sync --group test
uv run python -m signal_engine.pipeline --dry-run   # fetch only
uv run python -m signal_engine.pipeline           # full run
```

### Phase 0 exit criteria (before Phase 1)

- [ ] 3 consecutive weeks with ≥1 interview-worthy signal in digest
- [ ] At least 2 discovery calls booked from signals
- [ ] False-positive rate feels acceptable (<50% of “interview-worthy” are wastes of time)
- [ ] You open the digest 4+ days/week without forcing yourself

---

## Phase 1 — MVP product (10 beta users)

**Goal:** Founders with an active thesis pay €49/mo to replace manual pain scanning.

> **EU launch:** Shared Romanian SRL + compliance program with ComplianceForge. See [docs/EU_LAUNCH_PLAN.md](./docs/EU_LAUNCH_PLAN.md). ThesisRadar launches **after** ComplianceForge; EUR billing, Frankfurt data residency.

**Timeline:** 4–6 weeks after Phase 0 exit

### Build

| Feature | Priority |
|---------|----------|
| Thesis wizard (ICP, JTBD, competitors, keywords, disqualifiers) | P0 |
| Daily email digest (AgentMail) | P0 |
| Signal detail page with source receipts | P0 |
| Scorecard view (5 dimensions, not one number) | P0 |
| Auth + Stripe (€49/mo founding member, 20 seats cap) | P0 |
| Waitlist landing page | P0 |
| Web dashboard (Next.js) | P0 |

### Skip (resist scope creep)

- Generic idea browser
- Real-time alerts
- AI-generated business plans
- Public API
- Mobile app
- Multi-vertical packs

### Suggested stack (new surface)

| Layer | Choice | Notes |
|-------|--------|-------|
| App (fullstack) | **Next.js 14** App Router | UI, API routes, Server Actions, webhooks — single deploy surface |
| Signal engine | FastAPI wrapper over `signal-engine` | Internal service for ingestion + LLM scoring; called server-side only |
| DB | Postgres (Neon) + Prisma | Accessed from Next.js Server Components / Server Actions |
| Auth | Clerk | Middleware + Server Actions; keep separate from Vettd org auth |
| Billing | Stripe | Webhook route in Next.js (`/api/webhooks/stripe`) |
| Email | AgentMail | Daily digest via `signal-engine` LangGraph node (`docs/AGENTMAIL.md`) |
| Deploy | Vercel → **thesis-radar.intelliforge.tech** + Fly → thesis-radar-api.fly.dev | Independent from vettd-app.com |

### Repo strategy (parallel MVP)

```
IdeaForge/
├── signal-engine/          # Phase 0 CLI + shared Python package (keep)
├── apps/
│   └── thesis-radar/       # Phase 1 product
│       ├── web/            # Next.js fullstack (UI + API routes + Server Actions)
│       └── api/            # Python signal-engine HTTP service (internal)
```

Or split to `gengirish/thesis-radar` when billing/auth need clean separation.

### Success metric

- 10 beta users from network, **5 paying** at €49/mo
- 60% open digest 4+ days/week
- 3+ users schedule discovery calls from signals

### GTM (Phase 1 only)

- Personal outreach to founders doing customer discovery
- “I built this because PainHunt gives scores, not receipts + interview targets”
- No Product Hunt until Phase 2 retention holds

---

## Phase 2 — Retention & differentiation

**Goal:** Become **thesis monitoring**, not one-time validation.

**Timeline:** 6–8 weeks after Phase 1 launch

### Build

| Feature | Why |
|---------|-----|
| **Delta view** (“since yesterday”) | Creates daily habit |
| **Contradiction alerts** | “3 signals this week say manual phone screens work fine” — builds trust |
| **Interview pack export** | Signal → JTBD questions → outreach template |
| **Post-interview re-score** | User logs call outcome; thesis confidence updates |
| **Kill criteria** | User sets: “If X happens 3×, pause thesis” |
| G2 review scraper | Automate competitor weakness signals |
| Slack digest integration | Where founders live |

### Skip

- Idea generation marketplace
- VC portfolio mode (until Phase 3)

### Success metric

- 30-day retention **>50%**
- NPS ≥ 40 from users who ran ≥5 interviews sourced from signals

---

## Phase 3 — Scale wedge

**Goal:** Acquisition without you in every sale.

**Timeline:** 8–12 weeks after Phase 2 retention holds

### Build

| Feature | Details |
|---------|---------|
| **Vertical packs** | Recruiting, devtools, ecommerce ops — pre-tuned sources + keywords |
| **Public signal examples** | SEO pages: “Hair on fire problems in [vertical] — [month]” |
| **Scout tier** | €199/mo — 10 theses, team seats |
| **Lightweight API** | For VC associates |
| **Outcome tagging** | User marks pursued / killed / pivoted → feeds moat |

### Pricing (target)

| Tier | Price | Includes |
|------|-------|----------|
| Free | $0 | 1 thesis, weekly digest, 10 signals/mo |
| **Founder** | €79/mo | 3 theses, daily digest, full scorecard, outreach drafts |
| **Scout** | €199/mo | 10 theses, API, team seats |
| **Vertical pack** | +€49/mo | Pre-tuned sources per industry |

### GTM

- Weekly “Pain Radar” public reports per vertical (content = product demo)
- Founder community partnerships (Indie Hackers, YC alumni Slack)
- Product Hunt **after** retention proof

### Success metric

- 1 vertical pack published
- 3+ organic signups/week
- MRR $2K+ from ≥25 paying users

---

## Phase 4 — Moat & expansion

**Goal:** Compounding data advantage competitors can’t scrape overnight.

**Timeline:** Month 6+, only if Phase 2 retention holds

### Build

- **Outcome database** — “This pain cluster preceded 12 funded startups”
- **Human-in-the-loop QA tier** for VCs ($499/mo)
- Integrations: Notion, Linear, Slack, Clay (outreach)
- White-label for accelerators
- Reddit OAuth + official API (replace PullPush dependency)

### Moat layers

1. Proprietary signal corpus (dated, scored, tagged)
2. Outcome tracking (signal → funded startup)
3. Methodology IP (18startup + hair-on-fire rubric as product)
4. Vertical depth
5. Workflow lock-in (thesis history + interview logs)

---

## Parallel build playbook (with Vettd)

Use an explicit **time budget** so Vettd doesn’t stall:

| Rule | Recommendation |
|------|----------------|
| Time split | 80% Vettd / 20% Signal Engine until Phase 0 exit, then renegotiate |
| Shared infra | Same Neon Postgres (separate schema), same NVIDIA/Gemini keys |
| Shared learnings | Vettd discovery docs = Signal Engine thesis pack #1 |
| Separate brand | Never ship Signal Engine UI on vettd-app.com |
| Decision gate | Phase 1 starts only after Phase 0 exit criteria met |

### Weekly rhythm (Phase 0 → 1)

| Day | Signal Engine (30–60 min) |
|-----|----------------------------|
| Mon | Read digest; star 1 signal to pursue |
| Tue | Run 1 LinkedIn manual query from digest |
| Wed | Log outreach / interview outcome in tracker |
| Thu | Tune thesis YAML if false positives high |
| Fri | Update rolling synthesis in `CUSTOMER_DISCOVERY_TRACKER.md` |

---

## Risk register

| Risk | Mitigation |
|------|------------|
| Hallucinated evidence | Every signal links to source; no black-box scores |
| Idea tourist churn | Qualify in onboarding: “Do you have a thesis?” |
| Reddit/LinkedIn ToS | Diversify sources; store raw snapshots; OAuth in Phase 4 |
| Commodity collapse | Workflow + longitudinal data, not scores alone |
| Split focus with Vettd | Phase gates + time budget |
| False positives | Mandatory “already paying” + “pain real” fields |
| LLM cost at scale | Batch scoring; cheap model for extraction; cap daily scores |

---

## Key documents (cross-reference)

| Doc | Purpose |
|-----|---------|
| `signal-engine/README.md` | Phase 0 ops runbook |
| `docs/CUSTOMER_DISCOVERY_TRACKER.md` | Scorecard + interview log (Vettd dogfood) |
| `docs/HAIR_ON_FIRE_ANALYSIS.md` | Urgency analysis by segment |
| `docs/CUSTOMER_DISCOVERY_VALIDATION.md` | 18startup trait framework |
| `docs/SIGNAL_DIGEST.md` | Daily evidence log (generated) |

---

## 90-day checkpoint

| Week | Milestone |
|------|-----------|
| 3 | Phase 0 running daily; first real digest |
| 6 | Phase 0 exit criteria met OR thesis YAML tuned |
| 10 | Phase 1 landing page + waitlist live |
| 12 | 5 paying beta users; decision: spin out repo or stay monorepo |

---

## Next action (you)

1. **Run Phase 0 daily** until exit criteria hit (`uv run python -m signal_engine.pipeline`)
2. **Add GitHub secrets** for scheduled digest: `GEMINI_API_KEY`, `NVIDIA_NIM_API_KEY`, `DATABASE_URL`
3. **Book 2 interviews** from digest signals — this validates the product, not the code
4. When exit criteria met → start Phase 1 landing page + thesis wizard
