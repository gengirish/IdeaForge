# IntelliForge EU Launch Plan — Romanian SRL

> **Status tracker:** [EU_LAUNCH_STATUS.md](./EU_LAUNCH_STATUS.md) — checkboxes and “resume here” when you pick this up.
>
> **Scope:** One Romanian legal entity, one compliance program, one Stripe merchant account, **two products:**
> **ComplianceForge** (launch first) + **ThesisRadar** (launch second).
>
> **Not legal/tax advice.** Engage a Romanian accountant (TVA, OSS, e-Factura) and a GDPR lawyer before taking payment.

**Created:** 2026-06-23 · **Target:** ComplianceForge EU launch ~week 8–12 · ThesisRadar ~week 12–16

---

## Executive summary

| | ComplianceForge | ThesisRadar |
|---|-----------------|-------------|
| **Repo** | `D:\codebase\complianceforge` | `D:\codebase\IdeaForge` |
| **Buyer** | Eng / compliance leads shipping AI into EU | Founders with an active thesis |
| **Wedge** | EU AI Act Aug 2026 enforcement cliff | Receipts + interview targets, not idea scores |
| **Pricing (EU)** | €49 / €149 / €499 per month | €49/mo founding (20 seats) |
| **GTM in repo** | ✅ Strong (EUR, EU Act Explorer, CI wedge) | ✅ EUR in roadmap; EU GTM in this plan |
| **Launch order** | **#1** (weeks 8–12) | **#2** (weeks 12–16) |

**Strategy:** ComplianceForge brings deadline-driven EU demand and EUR billing on day one. ThesisRadar shares the same SRL, Stripe account, privacy pages, and Frankfurt Postgres pattern — different landing, same legal/ops backbone.

---

## One entity, shared backbone

```
┌─────────────────────────────────────────────────────────────┐
│  Romanian SRL (e.g. IntelliForge SRL) — data controller      │
│  ANSPDCP · TVA · OSS (B2C EU) · e-Factura (RO B2B)          │
└───────────────────────────┬─────────────────────────────────┘
                            │
     ┌──────────────────────┼──────────────────────┐
     ▼                      ▼                      ▼
┌─────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ Stripe RO   │    │ Shared legal    │    │ EU infra         │
│ EUR billing │    │ Privacy · ToS   │    │ Neon Frankfurt   │
│ Stripe Tax  │    │ Cookie banner   │    │ Fly fra (TR API) │
│ VAT ID B2B  │    │ Art. 30 register│    │ Vercel EU        │
└─────────────┘    │ Sub-processor   │    └──────────────────┘
                   │ list + DPAs     │
                   └─────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
    ┌──────────────────┐       ┌──────────────────┐
    │ ComplianceForge  │       │ ThesisRadar      │
    │ complianceforge  │       │ thesis-radar.*   │
    │ .app (target)    │       │ intelliforge.tech│
    └──────────────────┘       └──────────────────┘
```

### Shared (build once)

| Asset | Owner | Used by |
|-------|-------|---------|
| SRL registration, bank, VAT, OSS | Legal / accountant | Both |
| Stripe Romania merchant + Tax | Legal + eng | Both products, separate Price IDs |
| Privacy policy (controller = SRL) | Lawyer + eng | Both footers |
| Terms of service | Lawyer | Both |
| Cookie consent component | Eng | Both Next.js apps |
| Art. 30 processing register | Legal | Both |
| Sub-processor list + signed DPAs | Legal | Both |
| DSAR process (`privacy@…`) | Ops | Both |
| Neon Frankfurt project(s) | Eng | CF: Prisma · TR: signal-engine schema |
| e-Factura workflow | Accountant | All RO B2B invoices |

### Per-product (build twice)

| Asset | ComplianceForge | ThesisRadar |
|-------|-----------------|-------------|
| Landing + positioning | EU AI Act / CI wedge | Founder thesis wedge |
| Core product | Dashboard, AI Act Explorer, passport | Thesis wizard, digest, scorecard |
| Cron / pipeline | Evidence sync cron | LangGraph 4h signal pipeline |
| GTM outbound | Compliance officers, eng leads | Founders doing discovery |
| Domain | `complianceforge.app` | `thesis-radar.intelliforge.tech` |

---

## Phase overview

| Phase | Duration | Goal | Exit gate |
|-------|----------|------|-----------|
| **0** | 3–4 wks | Dogfood ThesisRadar + EU audit | TR Phase 0 exit criteria met |
| **1A** | 2–3 wks | Romanian SRL + tax | SRL live, VAT/OSS, e-Factura path |
| **1B** | 1–2 wks | EU infrastructure | Frankfurt DB + Fly `fra` + secrets |
| **1C** | 2 wks | Shared compliance surface | Privacy, ToS, cookies, Art. 30 |
| **1D-CF** | 4–6 wks | **ComplianceForge EU launch** | 5 paying @ €49+ |
| **1D-TR** | 4–6 wks | **ThesisRadar EU launch** | 5 paying @ €49 |
| **2** | 6–8 wks | Retention + EU ops maturity | >50% 30-day retention (combined) |
| **3** | 8–12 wks | EU acquisition | €4K+ combined MRR |

Phases **1A–1C** are shared. **1D** splits into two product tracks after shared gates pass.

---

## Phase 0 — Dogfood + EU audit (parallel start)

**Duration:** 3–4 weeks · **Can overlap with 1A**

### ThesisRadar (product validation)

| # | Task | Exit |
|---|------|------|
| 0.1 | Run pipeline daily (4h cron) | ✅ wired |
| 0.2 | 3 weeks ≥1 interview-worthy signal/week | ⬜ |
| 0.3 | 2 discovery calls booked from digest | ⬜ |
| 0.4 | False-positive rate acceptable on interview-worthy | ⬜ |
| 0.5 | Open digest 4+ days/week | ⬜ |

### Portfolio EU audit (both products)

| # | Task | Output |
|---|------|--------|
| 0.6 | Sub-processor inventory | Spreadsheet (see appendix) |
| 0.7 | Personal data map per product | CF: org, AI systems, VAT · TR: auth, thesis YAML |
| 0.8 | Auth decision | **Clerk + DPA** (shared) vs ZITADEL (defer) |
| 0.9 | Currency decision | **EUR only** for EU launch |
| 0.10 | e-Factura integrator | SmartBill / FGO / Oblio / accountant |
| 0.11 | Domain plan | CF: `complianceforge.app` · TR: existing subdomain |
| 0.12 | Launch order confirm | **ComplianceForge first** |

---

## Phase 1A — Romanian entity & tax

**Duration:** 2–3 weeks · **Start immediately**

| # | Task | Detail |
|---|------|--------|
| 1A.1 | Register **SRL** | CAEN 6201 (software / IT services) |
| 1A.2 | Bank accounts | RON + EUR for Stripe payouts |
| 1A.3 | ANAF registration | Fiscal ID |
| 1A.4 | VAT registration | Before EU B2C at scale |
| 1A.5 | **OSS** registration | EU B2C digital services |
| 1A.6 | Footer legal block | Company name, CUI, Reg. Com., RO address |
| 1A.7 | SPV + e-Factura access | Digital signature, ANAF portal |
| 1A.8 | e-Factura integrator | RO B2B within 5 working days |
| 1A.9 | Invoice numbering | ANAF-compliant series |

### Tax quick reference

| Customer | Treatment |
|----------|-----------|
| EU B2B + valid VAT ID | Reverse charge |
| EU B2C | Local VAT via OSS |
| Romania | 19% TVA |
| Non-EU | Accountant rules (export of services) |

**Exit:** SRL operational · VAT/OSS registered · e-Factura path defined (manual v1 OK)

---

## Phase 1B — EU infrastructure (shared)

**Duration:** 1–2 weeks · **After Phase 0 product signal OR in parallel with 1A**

### Postgres (Neon Frankfurt `aws-eu-central-1`)

| # | Task | Product |
|---|------|---------|
| 1B.1 | Create Neon project in Frankfurt | Shared account, **separate DBs** recommended: `complianceforge`, `thesis_radar` |
| 1B.2 | Migrate ComplianceForge Prisma schema | `npx prisma db push` on EU URL |
| 1B.3 | Migrate ThesisRadar signal schema | `signal_engine.db.init_schema()` |
| 1B.4 | Update all `DATABASE_URL` secrets | Vercel (both), Fly (TR API), GitHub Actions (TR cron) |
| 1B.5 | Verify TR cron writes to EU | `pipeline_runs` row after scheduled run |

### Compute

| # | Task | Product |
|---|------|---------|
| 1B.6 | Fly `primary_region = 'fra'` | ThesisRadar API (`apps/thesis-radar/api/fly.toml`) |
| 1B.7 | Redeploy + migrate machines | `fly scale count` / region move per Fly docs |
| 1B.8 | Vercel EU preference | Both projects |
| 1B.9 | AgentMail EU region | `https://api.agentmail.eu` where supported |

### ComplianceForge-specific

| # | Task | Note |
|---|------|------|
| 1B.10 | Confirm architecture doc matches prod | Already targets Vercel EU + Neon EU |
| 1B.11 | GitHub App webhooks | No region change; document in sub-processor list |

### DPAs (sign in parallel)

Neon · Fly · Vercel · Clerk · Stripe · Google · Anthropic · NVIDIA · AgentMail · GitHub

**Exit:** Customer data in Frankfurt · API in EU · DPAs signed · sub-processor list draft complete

---

## Phase 1C — Shared compliance surface

**Duration:** 2 weeks · **Depends on 1A.6 + 1B sub-processor list**

### Legal documents (lawyer: EN + RO)

| # | Document | Notes |
|---|----------|-------|
| 1C.1 | Privacy policy | Controller = RO SRL; both products; LLM disclosure |
| 1C.2 | Terms of service | Subscriptions, liability, RO/EU governing law |
| 1C.3 | Cookie policy | Clerk session cookies |
| 1C.4 | DPA template | For B2B customers requesting Art. 28 |

### Engineering (reusable package or copy)

| # | Task | Location |
|---|------|----------|
| 1C.5 | `/privacy` page | Both Next.js apps |
| 1C.6 | `/terms` page | Both |
| 1C.7 | Cookie consent banner | Shared component or duplicated |
| 1C.8 | Footer: legal entity + links | Both |
| 1C.9 | Sign-up consent checkbox | Both |
| 1C.10 | Account deletion flow | Clerk delete + product data cascade |

### Internal ops

| # | Task |
|---|------|
| 1C.11 | Art. 30 processing register (one doc, two processing activities) |
| 1C.12 | Transfer Impact Assessment (US subprocessors) |
| 1C.13 | DSAR playbook — `privacy@intelliforge.tech` (or `.ro`) |
| 1C.14 | Retention policy |

**Exit:** Legal pages live on both domains · DSAR process tested · marketing may claim **EU-hosted data (Frankfurt)**

---

## Phase 1D-CF — ComplianceForge launch (product #1)

**Duration:** 4–6 weeks · **Gate:** 1A + 1B + 1C complete

### Product (mostly built — ship + polish)

| # | Task | Priority |
|---|------|----------|
| 1D-CF.1 | Public landing (not redirect to sign-in) | P0 — see `UI-UX-IMPROVEMENT-PLAN-v2.md` |
| 1D-CF.2 | Enforcement countdown hero | P0 |
| 1D-CF.3 | Pricing page €49 / €149 / €499 | P0 |
| 1D-CF.4 | Stripe Checkout + Tax + VAT ID | P0 |
| 1D-CF.5 | 14-day trial flow | P0 |
| 1D-CF.6 | GitHub App listing (public) | P0 for CI wedge |
| 1D-CF.7 | FAQ: GDPR overlap, EU residency, self-host | P0 |
| 1D-CF.8 | Connect Neon EU + Vercel prod secrets | P0 |

### Stripe (shared merchant account)

| Product | Price ID | Amount |
|---------|----------|--------|
| CF Starter | `price_cf_starter` | €49/mo |
| CF Growth | `price_cf_growth` | €149/mo |
| CF Enterprise | `price_cf_enterprise` | €499/mo |

Use **metadata** `product=complianceforge` on subscriptions for reporting.

### GTM — ComplianceForge

| # | Channel | Message |
|---|---------|---------|
| GTM-CF.1 | Outbound to EU eng leads / CTOs | "Snyk for AI compliance — CI blocks non-compliant PRs" |
| GTM-CF.2 | SEO: `/act` AI Act Explorer | Organic top-of-funnel |
| GTM-CF.3 | Compliance passport virality | Every customer trust page = distribution |
| GTM-CF.4 | LinkedIn / founder networks in DE, NL, RO | Aug 2026 deadline urgency |
| GTM-CF.5 | **No Product Hunt** until Phase 2 retention | Discipline |

**Exit:** 10 beta orgs · **5 paying** at €49+ · e-Factura works for first RO B2B customer

---

## Phase 1D-TR — ThesisRadar launch (product #2)

**Duration:** 4–6 weeks · **Gate:** 1D-CF live OR 1D-CF in closed beta; 1C complete; Phase 0 exit

### Product (from `IDEA_DISCOVERY_ENGINE_ROADMAP.md`)

| # | Task | Priority |
|---|------|----------|
| 1D-TR.1 | Landing — EUR €49 founding, EU trust line | P0 |
| 1D-TR.2 | Thesis wizard → YAML | P0 |
| 1D-TR.3 | Multi-tenant schema (`users`, `theses`) | P0 |
| 1D-TR.4 | Per-user digest (AgentMail) | P0 |
| 1D-TR.5 | Signal detail + scorecard UI | P0 |
| 1D-TR.6 | Stripe founding plan (shared merchant) | P0 |
| 1D-TR.7 | Update roadmap USD → EUR | P0 |

| Product | Price ID | Amount |
|---------|----------|--------|
| TR Founding | `price_tr_founding` | €49/mo (20-seat cap) |

Metadata: `product=thesis-radar`

### GTM — ThesisRadar

| # | Channel | Message |
|---|---------|---------|
| GTM-TR.1 | Personal outreach to EU founders | "PainHunt gives scores; we give receipts + interview targets" |
| GTM-TR.2 | Qualify: "Do you have an active thesis?" | Filter idea tourists |
| GTM-TR.3 | Cross-sell from CF network | Founders building AI → TR for discovery; compliance buyers → CF |
| GTM-TR.4 | Dogfood digest as demo | `docs/SIGNAL_DIGEST.md` |

**Exit:** 10 beta users · **5 paying** @ €49 · 60% open digest 4+ days/week

---

## Phase 2 — Retention & EU ops maturity

**Duration:** 6–8 weeks after both 1D tracks

### Product

| ComplianceForge | ThesisRadar |
|-----------------|-------------|
| More evidence adapters (MLflow, W&B) | Dashboard delta + contradiction alerts |
| Passport custom domains | Interview pack export |
| Multi-reg graph (NIST, ISO) | Post-interview re-score |
| Compliance co-pilot | Kill criteria UI |

### EU operations

| # | Task | Frequency |
|---|------|-----------|
| 2.1 | OSS VAT return | Quarterly |
| 2.2 | e-Factura automation | Per RO B2B invoice |
| 2.3 | DSAR drill | Semi-annual |
| 2.4 | Sub-processor review | Annual |
| 2.5 | Combined MRR dashboard | Monthly |

**Exit:** >50% 30-day retention on paying cohort (either product)

---

## Phase 3 — EU acquisition

**Duration:** 8–12 weeks after Phase 2

| ComplianceForge | ThesisRadar |
|-----------------|-------------|
| Public SEO compliance reports | Vertical packs (recruiting, devtools) |
| Scout / enterprise tier | €79/mo Founder tier |
| Lightweight API for VC associates | Public "Pain Radar" pages |

**Combined target:** €4K+ MRR · 3+ organic signups/week across products

**Product Hunt:** only after Phase 2 retention holds.

---

## Workstream owners (2-founder split)

| Workstream | Primary | Weeks |
|------------|---------|-------|
| SRL + accountant + e-Factura | Business co-founder | 1A |
| DPAs + lawyer docs | Business co-founder | 1C |
| Neon + Fly EU migration | Technical co-founder | 1B |
| ComplianceForge 1D | Technical (product) + Business (GTM-CF) | 8–12 |
| ThesisRadar 1D | Technical (product) + Business (GTM-TR) | 12–16 |
| Vettd / India products | **Out of scope** — separate entity | — |

**Vettd time budget:** 80/20 until ThesisRadar Phase 0 exit, then renegotiate.

---

## 16-week calendar

| Week | Milestone |
|------|-----------|
| 1–2 | SRL filed · sub-processor spreadsheet · CF landing spec |
| 3 | Phase 0 exit OR thesis tuned · VAT/OSS registered |
| 4 | Neon Frankfurt live · Fly `fra` deployed |
| 5–6 | Privacy + ToS + cookies on CF staging |
| 7–8 | Stripe RO · CF public launch · first CF paying customer |
| 9–10 | TR thesis wizard + multi-tenant · shared legal on TR |
| 11–12 | TR founding plan live · 5 CF + 5 TR paying (stretch) |
| 13–16 | Phase 2 retention features · OSS first filing |

---

## Risk register

| Risk | Mitigation |
|------|------------|
| Split focus (2 products + Vettd) | **CF first**; TR only after 1C shared |
| e-Factura blocks RO B2B | Manual accountant v1; defer RO B2B until ready |
| US subprocessors (Clerk, LLMs) | DPAs + TIA; ZITADEL only if enterprise demands |
| CF landing redirects to sign-in | Fix before any paid traffic (`UI-UX-IMPROVEMENT-PLAN-v2`) |
| Two Neon DBs vs one | Separate DBs, same Frankfurt project/account — simpler blast radius |

---

## Appendix A — Sub-processors (shared list)

| Processor | Data | EU note |
|-----------|------|---------|
| Neon | DB | Frankfurt region |
| Vercel | Web hosting, logs | EU edge; US-HQ |
| Fly.io | TR API | `fra` |
| Clerk | Auth PII | US; DPF + SCCs |
| Stripe | Payment, VAT ID | Stripe Romania entity |
| Google Gemini | AI classification / scoring | US; DPA |
| Anthropic | CF doc gen | US; DPA |
| NVIDIA NIM | TR scoring | US; DPA |
| AgentMail | Email | Prefer EU API host |
| GitHub | CF CI webhooks, TR cron | US; DPA |

---

## Appendix B — Cross-references

| Doc | Repo |
|-----|------|
| `IDEA_DISCOVERY_ENGINE_ROADMAP.md` | IdeaForge |
| `docs/FEATURE-ROADMAP.md` | complianceforge |
| `docs/ARCHITECTURE.md` | complianceforge |
| `docs/UI-UX-IMPROVEMENT-PLAN-v2.md` | complianceforge |
| `docs/cursor-prompt.md` (EUR tiers) | complianceforge |
| `docs/AGENTMAIL.md` | IdeaForge |
| `docs/MOAT.md` | IdeaForge |

---

## Appendix C — Verification before "done"

```bash
# ThesisRadar
cd signal-engine && uv run pytest -q
cd apps/thesis-radar/web && npm run build

# ComplianceForge
cd complianceforge && npm run build && npm test
```

Each phase exit requires its checklist above — not just green CI.
