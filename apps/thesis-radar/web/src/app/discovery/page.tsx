import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Customer discovery for founders — ThesisRadar",
  description:
    "Daily evidence-grade signals for founders with an active thesis. Score hair-on-fire pain with receipts and know who to interview next.",
};

const founderProfiles = [
  {
    name: "Pre-PMF founder",
    bet: "Testing one ICP + JTBD hypothesis",
    pain: "Spends 2+ hours/day scanning Reddit and HN manually",
    outcome: "Books discovery calls from interview-worthy signals, not noise",
  },
  {
    name: "Indie hacker",
    bet: "Validating a niche before building",
    pain: "Validation tools give a score, not source receipts",
    outcome: "Sees who is already paying for workarounds in the wild",
  },
  {
    name: "PM / scout",
    bet: "Exploring a new vertical or product bet",
    pain: "One-time reports go stale the day after",
    outcome: "Daily delta and contradiction alerts keep the thesis honest",
  },
];

const scorecardFields = [
  { label: "Pain real?", detail: "Specific past instance, not vague annoyance" },
  { label: "Already paying?", detail: "Workaround spend is the strongest PMF signal" },
  { label: "Persona fit", detail: "Buyer, champion, or disqualifier hit" },
  { label: "Would pay?", detail: "Y / maybe / N — not a black-box 0–100" },
  { label: "Thesis fit", detail: "Supports, neutral, or contradicts your bet" },
];

const steps = [
  {
    step: "1",
    title: "Define your thesis",
    body: "ICP, problem hypothesis, keywords, competitors, and disqualifiers — not a random niche picker.",
  },
  {
    step: "2",
    title: "Ingest daily signals",
    body: "Reddit, HN, and review sources scored against your thesis, not generic idea trends.",
  },
  {
    step: "3",
    title: "Read the scorecard",
    body: "Five dimensions with linked source receipts. Every claim traceable.",
  },
  {
    step: "4",
    title: "Reach interview targets",
    body: "Signals that pass the interview-worthy gate include outreach angles and JTBD prompts.",
  },
];

export default function DiscoveryPage() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-16">
      <header className="mb-16">
        <p className="mb-2 text-sm font-medium uppercase tracking-widest text-brand-500">
          Customer discovery
        </p>
        <h1 className="mb-4 text-4xl font-bold tracking-tight sm:text-5xl">
          Evidence for founders who already have a bet
        </h1>
        <p className="max-w-2xl text-lg text-slate-400">
          ThesisRadar answers the question that matters before you write another line of code: is
          this problem hair-on-fire for your buyer — and who do you talk to next?
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            href="/sign-up"
            className="rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-brand-700"
          >
            Start founding member access
          </Link>
          <Link
            href="/dashboard"
            className="rounded-lg border border-slate-700 px-5 py-2.5 text-sm text-slate-200 transition hover:border-slate-500"
          >
            Preview signals
          </Link>
        </div>
      </header>

      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-semibold">Built for founders, not idea tourists</h2>
        <p className="mb-8 max-w-2xl text-slate-400">
          If you are browsing random niches for a startup idea, this is not for you. If you have a
          thesis and need daily evidence to stress-test it, you are the buyer.
        </p>
        <div className="grid gap-4 sm:grid-cols-3">
          {founderProfiles.map((profile) => (
            <article
              key={profile.name}
              className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
            >
              <h3 className="mb-3 font-semibold text-slate-100">{profile.name}</h3>
              <dl className="space-y-3 text-sm">
                <div>
                  <dt className="text-xs uppercase tracking-wide text-slate-500">Active bet</dt>
                  <dd className="mt-1 text-slate-300">{profile.bet}</dd>
                </div>
                <div>
                  <dt className="text-xs uppercase tracking-wide text-slate-500">Today</dt>
                  <dd className="mt-1 text-slate-400">{profile.pain}</dd>
                </div>
                <div>
                  <dt className="text-xs uppercase tracking-wide text-brand-500">With ThesisRadar</dt>
                  <dd className="mt-1 text-slate-200">{profile.outcome}</dd>
                </div>
              </dl>
            </article>
          ))}
        </div>
      </section>

      <section className="mb-16 rounded-xl border border-slate-800 bg-slate-900/30 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">Why one-time validation fails</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Most tools optimize for a single 0–100 score on a broad niche. Customer discovery is
          longitudinal — you need receipts, contradictions, and kill criteria as your thesis evolves.
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
              {[
                ["Broad niche → idea suggestions", "Your ICP + JTBD → urgency evidence"],
                ["Single validation score", "Scorecard: pain, frequency, spend, fit, would pay"],
                ["One-time report", "Daily delta + contradiction alerts"],
                ["Idea generation", "Signal → interview target → outreach angle"],
              ].map(([them, us]) => (
                <tr key={them} className="border-b border-slate-800/60">
                  <td className="py-3 pr-4 text-slate-500">{them}</td>
                  <td className="py-3 text-slate-200">{us}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mb-16">
        <h2 className="mb-8 text-2xl font-semibold">How discovery works</h2>
        <ol className="grid gap-4 sm:grid-cols-2">
          {steps.map((item) => (
            <li
              key={item.step}
              className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
            >
              <span className="mb-3 inline-flex h-8 w-8 items-center justify-center rounded-full bg-brand-900/60 text-sm font-semibold text-brand-500">
                {item.step}
              </span>
              <h3 className="mb-2 font-semibold">{item.title}</h3>
              <p className="text-sm text-slate-400">{item.body}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-semibold">Interview-worthy gate</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Signals only surface for outreach when they pass evidence thresholds — not when an LLM
          feels optimistic.
        </p>
        <ul className="grid gap-3 sm:grid-cols-2">
          {scorecardFields.map((field) => (
            <li
              key={field.label}
              className="rounded-lg border border-slate-800 bg-slate-900/30 px-4 py-3"
            >
              <p className="font-medium text-slate-200">{field.label}</p>
              <p className="mt-1 text-sm text-slate-500">{field.detail}</p>
            </li>
          ))}
        </ul>
        <p className="mt-4 text-sm text-slate-500">
          Gate: pain real + buyer/champion + would pay (Y or maybe) + urgency ≥ 3 + frequency ≥
          monthly + no disqualifier hit.
        </p>
      </section>

      <section className="rounded-xl border border-brand-900/50 bg-brand-900/10 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">Founding member — $49/mo</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Twenty seats. Daily digest, full scorecard, thesis wizard, and source receipts. Replace
          manual pain scanning with evidence you would stake an interview on.
        </p>
        <Link
          href="/sign-up"
          className="inline-flex rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-brand-700"
        >
          Join as a founding founder
        </Link>
      </section>
    </main>
  );
}
