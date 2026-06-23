# EU Launch — Status & Resume Here

> **Full plan:** [EU_LAUNCH_PLAN.md](./EU_LAUNCH_PLAN.md)  
> **Last updated:** 2026-06-23  
> **Paused — resume when ready.** No blockers in code; legal/entity work is the critical path.

---

## When you come back

1. Read **Current focus** below.
2. Do the **Next 3 actions**.
3. Check boxes as you complete items.
4. Update **Last updated** at the top of this file.

---

## Current focus

| Field | Value |
|-------|-------|
| **Active phase** | Phase 0 (dogfood) + Phase 1A (SRL) in parallel |
| **Launch order** | ComplianceForge first → ThesisRadar second |
| **Entity** | Romanian SRL (not started) |
| **Infra** | Fly `fra` in `fly.toml` ✅ · Neon Frankfurt ⬜ · redeploy API ⬜ |

---

## Next 3 actions (start here)

- [ ] **1A** Engage Romanian accountant; begin SRL registration (CAEN 6201)
- [ ] **0** Complete sub-processor spreadsheet (see plan Appendix A)
- [ ] **0** Book 1 discovery call from ThesisRadar digest (validates product before EU spend)

---

## Phase checklist

### Phase 0 — Dogfood + EU audit (3–4 wks)

- [ ] 3 weeks ≥1 interview-worthy signal/week (ThesisRadar)
- [ ] 2 discovery calls booked from digest
- [ ] False-positive rate acceptable
- [ ] Open digest 4+ days/week
- [ ] Sub-processor inventory done
- [ ] Auth strategy: Clerk + DPA (documented)
- [ ] e-Factura integrator chosen
- [ ] Launch order confirmed: CF → TR

### Phase 1A — Romanian entity & tax (2–3 wks)

- [ ] SRL registered
- [ ] Bank (RON + EUR)
- [ ] ANAF / fiscal ID
- [ ] VAT registered
- [ ] OSS registered (if B2C EU)
- [ ] e-Factura path (manual v1 OK)
- [ ] Footer legal text drafted

### Phase 1B — EU infrastructure (1–2 wks)

- [ ] Neon project `aws-eu-central-1` (Frankfurt)
- [ ] ComplianceForge DB on EU Neon
- [ ] ThesisRadar DB on EU Neon
- [ ] `DATABASE_URL` updated (Vercel, Fly, GitHub Actions)
- [ ] Fly API redeployed to `fra` (`npm run deploy:api`)
- [ ] DPAs signed (Neon, Vercel, Clerk, Stripe, LLM providers, AgentMail, GitHub)

### Phase 1C — Shared compliance (2 wks)

- [ ] Privacy policy (lawyer, EN + RO)
- [ ] Terms of service
- [ ] Cookie policy + banner (both apps)
- [ ] `/privacy` + `/terms` on ComplianceForge
- [ ] `/privacy` + `/terms` on ThesisRadar
- [ ] Art. 30 processing register
- [ ] DSAR process (`privacy@…`)
- [ ] Account deletion flow

### Phase 1D-CF — ComplianceForge launch (4–6 wks)

- [ ] Public landing (not sign-in redirect)
- [ ] Pricing €49 / €149 / €499
- [ ] Stripe RO + Tax + VAT ID at checkout
- [ ] 14-day trial
- [ ] GitHub App public listing
- [ ] 5 paying customers @ €49+

### Phase 1D-TR — ThesisRadar launch (4–6 wks)

- [ ] Landing EUR €49 founding
- [ ] Thesis wizard + multi-tenant DB
- [ ] Per-user digest (AgentMail)
- [ ] Scorecard UI
- [ ] Stripe founding plan (shared merchant)
- [ ] 5 paying @ €49

### Phase 2 — Retention (6–8 wks)

- [ ] >50% 30-day retention (paying cohort)
- [ ] First quarterly OSS VAT filing
- [ ] e-Factura automation (or stable manual process)

### Phase 3 — EU scale (8–12 wks)

- [ ] Combined €4K+ MRR
- [ ] 3+ organic signups/week

---

## Repo quick links

| Repo | Path | Role |
|------|------|------|
| **Plan (canonical)** | `IdeaForge/docs/EU_LAUNCH_PLAN.md` | Full phased plan |
| **ThesisRadar** | `IdeaForge/` | Signal engine + web |
| **ComplianceForge** | `complianceforge/` | EU AI Act SaaS (launch #1) |
| **CF launch UX** | `complianceforge/docs/UI-UX-IMPROVEMENT-PLAN-v2.md` | Landing before paid traffic |
| **TR roadmap** | `IdeaForge/IDEA_DISCOVERY_ENGINE_ROADMAP.md` | Product phases |

---

## Decisions log

| Date | Decision | Notes |
|------|----------|-------|
| 2026-06-23 | One Romanian SRL for both products | Shared Stripe, privacy, Frankfurt DB |
| 2026-06-23 | ComplianceForge launches before ThesisRadar | Deadline-driven EU demand |
| 2026-06-23 | EUR only for EU launch | OSS for B2C |
| 2026-06-23 | Clerk + DPA (not ZITADEL yet) | Revisit if enterprise requires EU-only auth |
| 2026-06-23 | Fly `primary_region = fra` | Redeploy pending |

---

## Out of scope (separate India entity)

Vettd · AwaazOS · MoveMore · AyushOS · DropFlow · ChairOS · FacilityOS — INR / India stack.
