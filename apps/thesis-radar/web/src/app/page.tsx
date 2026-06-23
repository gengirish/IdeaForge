import Link from "next/link";

import { PipelineLiveStats } from "@/components/pipeline-live-stats";

export const revalidate = 300;

const pipelineStats = [
  { label: "Pipeline cadence", value: "6 runs/day", detail: "Every 4h cron in production" },
  { label: "Signal sources", value: "Reddit, HN, G2", detail: "Scored against your thesis" },
  { label: "Scoring stack", value: "LangGraph + NIM", detail: "NVIDIA NIM → Gemini fallback" },
  { label: "Corpus", value: "Postgres (Neon)", detail: "Time-series evidence store" },
];

const comparisonRows = [
  ["Broad niche → idea suggestions", "Your ICP + JTBD → urgency evidence"],
  ["Single 0–100 validation score", "Scorecard: pain, spend, fit, would pay"],
  ["One-time report", "Daily delta + contradiction alerts"],
  ["Manual Reddit/HN scanning", "Signal → interview target → outreach angle"],
];

const moatBullets = [
  {
    title: "Time-series corpus",
    body: "Every signal stored with receipts — not a one-off scrape that goes stale tomorrow.",
  },
  {
    title: "Scorecard, not 0–100",
    body: "Five evidence dimensions with linked sources. No black-box optimism.",
  },
  {
    title: "Daily delta",
    body: "Contradiction alerts and kill criteria as your thesis evolves.",
  },
];

const footerLinks = [
  { href: "/about", label: "About" },
  { href: "/how-it-works", label: "How it works" },
  { href: "/examples", label: "Examples" },
  { href: "/discovery", label: "Discovery" },
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-16">
      {/* Hero — PAS: problem (manual scanning), agitate (one-time scores), solution (ThesisRadar) */}
      <header className="mb-16">
        <p className="mb-1 text-sm font-medium uppercase tracking-widest text-brand-500">
          IntelliForge · ThesisRadar
        </p>
        <p className="mb-4 text-sm text-slate-500">
          Customer discovery software — not hardware radar
        </p>
        <h1 className="mb-4 text-4xl font-bold tracking-tight sm:text-5xl">
          Daily evidence for founders who already have a bet
        </h1>
        <p className="max-w-2xl text-lg text-slate-400">
          You spend hours scanning Reddit and HN by hand — or you get a one-time validation score
          with no receipts. ThesisRadar is thesis-driven customer discovery SaaS: daily signals
          scored against your ICP and JTBD, with source links you would stake an interview on.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            href="/discovery"
            className="rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-brand-700"
          >
            See how discovery works
          </Link>
          <Link
            href="/sign-up"
            className="rounded-lg border border-slate-700 px-5 py-2.5 text-sm text-slate-200 transition hover:border-slate-500"
          >
            Start founding member access
          </Link>
        </div>
      </header>

      {/* Pipeline in production */}
      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-semibold">Pipeline in production</h2>
        <p className="mb-8 max-w-2xl text-slate-400">
          Phase 0 dogfood — honest numbers from the live signal engine, not a slide deck.
        </p>
        <PipelineLiveStats />
        <div className="grid gap-4 sm:grid-cols-2">
          {pipelineStats.map((stat) => (
            <article
              key={stat.label}
              className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
            >
              <p className="text-xs uppercase tracking-wide text-slate-500">{stat.label}</p>
              <p className="mt-2 font-semibold text-slate-100">{stat.value}</p>
              <p className="mt-1 text-sm text-slate-400">{stat.detail}</p>
            </article>
          ))}
        </div>
      </section>

      {/* Problem / wedge */}
      <section className="mb-16 rounded-xl border border-slate-800 bg-slate-900/30 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">Built for founders, not idea tourists</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Most tools optimize for a single score on a broad niche. Customer discovery is
          longitudinal — you need receipts, contradictions, and kill criteria as your thesis
          evolves.
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
              {comparisonRows.map(([them, us]) => (
                <tr key={them} className="border-b border-slate-800/60">
                  <td className="py-3 pr-4 text-slate-500">{them}</td>
                  <td className="py-3 text-slate-200">{us}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Moat teaser */}
      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-semibold">Why the corpus compounds</h2>
        <p className="mb-8 max-w-2xl text-slate-400">
          ThesisRadar is not a wrapper on a one-shot LLM prompt. The moat is longitudinal evidence.
        </p>
        <ul className="grid gap-4 sm:grid-cols-3">
          {moatBullets.map((item) => (
            <li
              key={item.title}
              className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
            >
              <h3 className="mb-2 font-semibold text-slate-100">{item.title}</h3>
              <p className="text-sm text-slate-400">{item.body}</p>
            </li>
          ))}
        </ul>
        <p className="mt-6 text-sm">
          <Link href="/how-it-works" className="text-brand-500 transition hover:text-brand-700">
            How the signal engine works →
          </Link>
        </p>
      </section>

      {/* Market wedge */}
      <section className="mb-16 rounded-xl border border-brand-900/50 bg-brand-900/10 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">Founding member — $49/mo</h2>
        <p className="mb-4 max-w-2xl text-slate-400">
          Pre-PMF founders with an active thesis — not niche browsers looking for startup ideas.
          Twenty seats at founding pricing: daily digest, full scorecard, thesis wizard, and source
          receipts.
        </p>
        <p className="mb-6 text-sm text-slate-500">
          First vertical dogfood: recruiting &amp; talent acquisition — where pain signals are loud
          on Reddit and G2.
        </p>
        <Link
          href="/sign-up"
          className="inline-flex rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-brand-700"
        >
          Join as a founding founder
        </Link>
      </section>

      {/* Proof CTA */}
      <section className="mb-16 rounded-xl border border-slate-800 bg-slate-900/30 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">See real digests</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Sample daily digests with scorecards and source receipts — evidence you can evaluate
          before you sign up.
        </p>
        <Link
          href="/examples"
          className="inline-flex rounded-lg border border-slate-700 px-5 py-2.5 text-sm text-slate-200 transition hover:border-slate-500"
        >
          Browse example digests
        </Link>
      </section>

      {/* Footer links */}
      <footer className="border-t border-slate-800 pt-8">
        <nav className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-500">
          {footerLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="transition hover:text-slate-300"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <p className="mt-4 text-xs text-slate-600">
          ThesisRadar by IntelliForge — customer discovery SaaS for thesis-driven founders.
        </p>
      </footer>
    </main>
  );
}
