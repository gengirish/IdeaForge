import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "How ThesisRadar works — evidence-grade customer discovery",
  description:
    "From Reddit, HN, and review sources to interview targets: thesis-driven ingestion, LangGraph scoring, scorecard rubric, and daily digest.",
  keywords: ["customer discovery", "thesis validation", "scorecard"],
};

const architectureSteps = [
  {
    step: "1",
    title: "Sources",
    body: "Reddit, Hacker News, and G2 reviews — public pain signals tied to your thesis keywords.",
  },
  {
    step: "2",
    title: "Ingestion & dedupe",
    body: "Fetch, normalize, and upsert by source ID into Postgres. Re-seen posts still grow the corpus.",
  },
  {
    step: "3",
    title: "LangGraph scoring",
    body: "Evidence extraction and rubric scoring via NVIDIA NIM with Gemini fallback — not a black-box 0–100.",
  },
  {
    step: "4",
    title: "Scorecard",
    body: "Eight rubric fields: pain real, frequency, expensive, paying, persona fit, would pay, thesis fit, urgency.",
  },
  {
    step: "5",
    title: "Daily digest",
    body: "Email and dashboard summary with source receipts, delta since yesterday, and contradiction alerts.",
  },
  {
    step: "6",
    title: "Interview targets",
    body: "Signals that pass the interview-worthy gate ship with outreach angles and JTBD prompts.",
  },
];

const scorecardRubric = [
  {
    field: "Pain real?",
    values: "Y / N",
    meaning: "Specific past instance, not vague annoyance",
  },
  {
    field: "Pain frequent?",
    values: "weekly / monthly / rare",
    meaning: "How often the buyer hits the problem",
  },
  {
    field: "Pain expensive?",
    values: "Y / N",
    meaning: "Quantified cost — hours, money, or lost deals",
  },
  {
    field: "Already paying?",
    values: "Y / N",
    meaning: "Workaround spend is the strongest PMF signal",
  },
  {
    field: "Persona fit",
    values: "buyer / champion / user-only / not-fit",
    meaning: "Whether the speaker matches your ICP",
  },
  {
    field: "Would pay?",
    values: "Y / maybe / N",
    meaning: "Stated willingness to pay for relief",
  },
  {
    field: "Thesis fit",
    values: "supports / neutral / contradicts",
    meaning: "Strengthens or kills your hypothesis",
  },
  {
    field: "Urgency",
    values: "1–5",
    meaning: "Composite hair-on-fire score",
  },
];

const moatLayers = [
  {
    title: "Time-series signal corpus",
    body: "Raw and scored signals upserted into Postgres every 2 hours — twelve runs per day. The corpus compounds even when posts are re-seen.",
  },
  {
    title: "Thesis YAML rotation",
    body: "Each slot round-robins your thesis configs — ICP, disqualifiers, problem hypothesis, and kill criteria stay in the loop.",
  },
  {
    title: "Daily delta & contradiction alerts",
    body: "Since-yesterday changes, signals that contradict your bet, and kill-criteria triggers — accuracy deepens as 7d/14d history grows.",
  },
  {
    title: "Labeled corpus, not commodity LLM",
    body: "Anyone can call an LLM scorer. Competitors cannot replicate your dated, scored, thesis-tagged evidence without your labels and time depth.",
  },
];

const competitorRows = [
  ["Broad niche → idea suggestions", "Your ICP + JTBD thesis → urgency evidence"],
  ["Single 0–100 score", "Scorecard: pain real, frequency, expensive, paying, would pay"],
  ["One-time validation report", "Daily delta + contradiction alerts"],
  ["Idea generation", "Signal → interview target → outreach angle"],
];

export default function HowItWorksPage() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-16">
      <header className="mb-16">
        <p className="mb-2 text-sm font-medium uppercase tracking-widest text-brand-500">
          How it works
        </p>
        <h1 className="mb-4 text-4xl font-bold tracking-tight sm:text-5xl">
          How ThesisRadar works
        </h1>
        <p className="max-w-2xl text-lg text-slate-400">
          A thesis-driven, evidence-grade signal engine — not another “validate any idea in 10
          seconds” tool. Daily receipts for founders who already have a bet.
        </p>
      </header>

      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-semibold">Architecture flow</h2>
        <p className="mb-8 max-w-2xl text-slate-400">
          Public sources flow through ingestion and LangGraph scoring, anchored by your thesis YAML.
          Only signals with receipts reach your digest and outreach queue.
        </p>

        <div className="hidden gap-0 lg:grid lg:grid-cols-[1fr_auto_1fr_auto_1fr_auto_1fr_auto_1fr_auto_1fr] lg:items-stretch">
          {architectureSteps.map((item, index) => (
            <div key={item.step} className="contents">
              <article className="flex flex-col rounded-xl border border-slate-800 bg-slate-900/40 p-4">
                <span className="mb-2 inline-flex h-7 w-7 items-center justify-center rounded-full bg-brand-900/60 text-xs font-semibold text-brand-500">
                  {item.step}
                </span>
                <h3 className="mb-1 text-sm font-semibold text-slate-100">{item.title}</h3>
                <p className="text-xs leading-relaxed text-slate-500">{item.body}</p>
              </article>
              {index < architectureSteps.length - 1 && (
                <div
                  className="flex items-center justify-center px-1 text-slate-600"
                  aria-hidden="true"
                >
                  →
                </div>
              )}
            </div>
          ))}
        </div>

        <ol className="grid gap-4 sm:grid-cols-2 lg:hidden">
          {architectureSteps.map((item) => (
            <li
              key={item.step}
              className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
            >
              <span className="mb-3 inline-flex h-8 w-8 items-center justify-center rounded-full bg-brand-900/60 text-sm font-semibold text-brand-500">
                {item.step}
              </span>
              <h3 className="mb-2 font-semibold text-slate-100">{item.title}</h3>
              <p className="text-sm text-slate-400">{item.body}</p>
            </li>
          ))}
        </ol>

        <p className="mt-6 rounded-lg border border-slate-800 bg-slate-900/30 px-4 py-3 text-sm text-slate-500">
          <span className="font-medium text-slate-400">Thesis YAML</span> — ICP, disqualifiers,
          problem hypothesis, and kill criteria — feeds ingestion filters and scoring context at
          every run.
        </p>
      </section>

      <section className="mb-16 rounded-xl border border-slate-800 bg-slate-900/30 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">Scorecard rubric</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Every signal is scored on explicit dimensions mapped to the 18startup validation
          framework — hair on fire, budget exists, accessible buyer, urgency, and specificity.
        </p>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[36rem] text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-slate-500">
                <th className="pb-3 pr-4 font-medium">Field</th>
                <th className="pb-3 pr-4 font-medium">Values</th>
                <th className="pb-3 font-medium">Meaning</th>
              </tr>
            </thead>
            <tbody className="text-slate-300">
              {scorecardRubric.map((row) => (
                <tr key={row.field} className="border-b border-slate-800/60">
                  <td className="py-3 pr-4 font-medium text-slate-200">{row.field}</td>
                  <td className="py-3 pr-4 text-slate-500">{row.values}</td>
                  <td className="py-3 text-slate-400">{row.meaning}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-semibold">Interview-worthy gate</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Signals surface for outreach only when they pass evidence thresholds — not when an LLM
          feels optimistic. This is how ThesisRadar filters noise before you book a discovery call.
        </p>
        <div className="rounded-xl border border-brand-900/40 bg-brand-900/10 p-6">
          <p className="mb-4 text-sm font-medium uppercase tracking-wide text-brand-500">
            All conditions required
          </p>
          <ul className="space-y-3 text-sm text-slate-300">
            <li className="flex gap-3">
              <span className="text-brand-500" aria-hidden="true">
                ✓
              </span>
              <span>
                <strong className="text-slate-200">Pain real</strong> — specific past instance, not
                vague annoyance
              </span>
            </li>
            <li className="flex gap-3">
              <span className="text-brand-500" aria-hidden="true">
                ✓
              </span>
              <span>
                <strong className="text-slate-200">Persona fit</strong> — buyer or champion (not
                user-only or not-fit)
              </span>
            </li>
            <li className="flex gap-3">
              <span className="text-brand-500" aria-hidden="true">
                ✓
              </span>
              <span>
                <strong className="text-slate-200">Would pay</strong> — Y or maybe
              </span>
            </li>
            <li className="flex gap-3">
              <span className="text-brand-500" aria-hidden="true">
                ✓
              </span>
              <span>
                <strong className="text-slate-200">Urgency</strong> — score ≥ 3
              </span>
            </li>
            <li className="flex gap-3">
              <span className="text-brand-500" aria-hidden="true">
                ✓
              </span>
              <span>
                <strong className="text-slate-200">Frequency</strong> — at least monthly (not rare)
              </span>
            </li>
            <li className="flex gap-3">
              <span className="text-brand-500" aria-hidden="true">
                ✓
              </span>
              <span>
                <strong className="text-slate-200">No disqualifier hit</strong> — thesis YAML
                exclusion rules not triggered
              </span>
            </li>
          </ul>
          <p className="mt-5 text-sm text-slate-500">
            A signal that passes is tagged as a{" "}
            <span className="text-slate-400">3-yes signal</span>: pain real + buyer/champion +
            would pay — the minimum bar before outreach.
          </p>
        </div>
      </section>

      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-semibold">Moat: what compounds</h2>
        <p className="mb-8 max-w-2xl text-slate-400">
          Defensibility is not the LLM scorer — that is commodity. It is the proprietary,
          time-series evidence corpus tied to explicit theses.
        </p>
        <div className="grid gap-4 sm:grid-cols-2">
          {moatLayers.map((layer) => (
            <article
              key={layer.title}
              className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
            >
              <h3 className="mb-2 font-semibold text-slate-100">{layer.title}</h3>
              <p className="text-sm text-slate-400">{layer.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="mb-16 rounded-xl border border-slate-800 bg-slate-900/30 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">ThesisRadar vs PainHunt & GapFinder</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Competitors optimize for idea tourists browsing niches. ThesisRadar optimizes for founders
          stress-testing an active bet with longitudinal evidence.
        </p>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[32rem] text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-slate-500">
                <th className="pb-3 pr-4 font-medium">They optimize for</th>
                <th className="pb-3 font-medium">ThesisRadar optimizes for</th>
              </tr>
            </thead>
            <tbody className="text-slate-300">
              {competitorRows.map(([them, us]) => (
                <tr key={them} className="border-b border-slate-800/60">
                  <td className="py-3 pr-4 text-slate-500">{them}</td>
                  <td className="py-3 text-slate-200">{us}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="rounded-xl border border-brand-900/50 bg-brand-900/10 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">See it in action</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Browse real signal examples from the recruiting/TA dogfood thesis, or start your own
          evidence-grade discovery loop.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/examples"
            className="rounded-lg border border-slate-700 px-5 py-2.5 text-sm text-slate-200 transition hover:border-slate-500"
          >
            View signal examples
          </Link>
          <Link
            href="/sign-up"
            className="rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-brand-700"
          >
            Start founding member access
          </Link>
        </div>
      </section>
    </main>
  );
}
