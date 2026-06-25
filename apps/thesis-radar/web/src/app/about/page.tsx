import type { Metadata } from "next";
import Link from "next/link";

import { FounderCard } from "@/components/founder-card";

export const metadata: Metadata = {
  title: "About IntelliForge & ThesisRadar",
  description:
    "IntelliForge builds B2B software. ThesisRadar is customer discovery SaaS for founders — built by Girish Hiremath, AI practitioner with 14+ years shipping enterprise systems.",
};

const whyBuilt = [
  {
    title: "Dogfooding on real discovery",
    body: "We run ThesisRadar on our own recruiting/TA thesis in signal-engine — the same customer discovery work behind Vettd. Phase 0 shipped a daily digest we actually read.",
  },
  {
    title: "Manual scanning does not scale",
    body: "Founders spend 2+ hours a day scanning Reddit, HN, and forums for pain signals. That time should go to interviews, not tab-hopping.",
  },
  {
    title: "Scores without receipts fail",
    body: "One-time validation tools hand you a 0–100 score with no source links. Customer discovery needs evidence you can cite in a call — not a black-box number.",
  },
];

const roadmapMilestones = [
  {
    phase: "Phase 0",
    timeline: "Shipped",
    goal: "Prove the loop on ourselves (recruiting/TA dogfood)",
    exitMetrics:
      "≥1 interview-worthy signal/week for 3 consecutive weeks · 2+ discovery calls booked from digest · <50% false-positive rate on interview-worthy · digest opened 4+ days/week",
  },
  {
    phase: "Phase 1",
    timeline: "Months 1–2",
    goal: "MVP — replace manual pain scanning",
    exitMetrics:
      "10 beta users · 5+ paying @ $49/mo founding · 60% open digest 4+ days/week · 3+ users schedule discovery calls from signals",
  },
  {
    phase: "Phase 2",
    timeline: "Months 3–5",
    goal: "Retention & multi-thesis monitoring",
    exitMetrics:
      ">50% 30-day retention · delta view + contradiction alerts · interview pack export · kill criteria",
  },
  {
    phase: "Phase 3",
    timeline: "Months 6–9",
    goal: "Repeatable acquisition",
    exitMetrics:
      "Vertical packs · public signal examples for SEO · €4K+ combined portfolio MRR (EU launch plan)",
  },
  {
    phase: "Phase 4",
    timeline: "Months 12–18",
    goal: "Moat — outcome database & API",
    exitMetrics:
      "Proprietary signal corpus · outcome tracking (signal → funded startup) · lightweight API for scouts and VCs",
  },
];

export default function AboutPage() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-16">
      <header className="mb-16">
        <p className="mb-2 text-sm font-medium uppercase tracking-widest text-brand-500">
          About
        </p>
        <h1 className="mb-4 text-4xl font-bold tracking-tight sm:text-5xl">
          IntelliForge builds software. ThesisRadar is customer discovery.
        </h1>
        <p className="max-w-2xl text-lg text-slate-400">
          IntelliForge is a Romanian SRL building B2B software — ThesisRadar today, plus future
          products under a shared EU compliance backbone (see ComplianceForge in our launch plan).
          ThesisRadar is a thesis-driven daily signal engine for founders doing customer discovery.
        </p>
        <p className="mt-4 max-w-2xl rounded-lg border border-slate-800 bg-slate-900/40 px-4 py-3 text-sm text-slate-300">
          <span className="font-medium text-slate-100">Clarification: </span>
          ThesisRadar is software for customer discovery. We do not build radar sensors or defense
          hardware.
        </p>
      </header>

      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-semibold">Company vs product</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          IntelliForge is the legal entity and engineering company. ThesisRadar is the product
          surface at thesis-radar.intelliforge.tech — separate from vettd-app.com.
        </p>
        <div className="grid gap-4 sm:grid-cols-2">
          <article className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
            <h3 className="mb-2 font-semibold text-brand-500">IntelliForge</h3>
            <p className="text-sm text-slate-400">
              Romanian SRL · B2B software · EU-hosted data (Frankfurt) · shared Stripe, privacy,
              and compliance program across portfolio products.
            </p>
          </article>
          <article className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
            <h3 className="mb-2 font-semibold text-brand-500">ThesisRadar</h3>
            <p className="text-sm text-slate-400">
              Daily evidence-grade signals for founders with an active thesis — scorecard with
              source receipts, interview targets, and contradiction alerts. Not idea generation.
            </p>
          </article>
        </div>
      </section>

      <section className="mb-16">
        <h2 className="mb-8 text-2xl font-semibold">Why we built this</h2>
        <ol className="grid gap-4">
          {whyBuilt.map((item, index) => (
            <li
              key={item.title}
              className="rounded-xl border border-slate-800 bg-slate-900/40 p-5"
            >
              <span className="mb-3 inline-flex h-8 w-8 items-center justify-center rounded-full bg-brand-900/60 text-sm font-semibold text-brand-500">
                {index + 1}
              </span>
              <h3 className="mb-2 font-semibold">{item.title}</h3>
              <p className="text-sm text-slate-400">{item.body}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="mb-16 rounded-xl border border-slate-800 bg-slate-900/30 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">Founder</h2>
        <p className="mb-8 max-w-2xl text-slate-400">
          ThesisRadar is built by engineers who ship production AI systems — not slide-deck
          validators.
        </p>
        <FounderCard />
      </section>

      <section className="mb-16">
        <h2 className="mb-2 text-2xl font-semibold">Roadmap — next 12–18 months</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Phases gate on evidence, not vanity launches. Phase 1 starts only after Phase 0 exit
          criteria are met.
        </p>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[40rem] text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-slate-500">
                <th className="pb-3 pr-4 font-medium">Phase</th>
                <th className="pb-3 pr-4 font-medium">Timeline</th>
                <th className="pb-3 pr-4 font-medium">Goal</th>
                <th className="pb-3 font-medium">Exit metrics</th>
              </tr>
            </thead>
            <tbody className="text-slate-300">
              {roadmapMilestones.map((row) => (
                <tr key={row.phase} className="border-b border-slate-800/60">
                  <td className="py-3 pr-4 font-medium text-brand-500">{row.phase}</td>
                  <td className="py-3 pr-4 text-slate-400">{row.timeline}</td>
                  <td className="py-3 pr-4 text-slate-200">{row.goal}</td>
                  <td className="py-3 text-slate-400">{row.exitMetrics}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="rounded-xl border border-brand-900/50 bg-brand-900/10 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">See it in action</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Read how customer discovery works, or join as a founding member and replace manual pain
          scanning with daily evidence.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/sign-up"
            className="rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-brand-700"
          >
            Start founding member access
          </Link>
          <Link
            href="/discovery"
            className="rounded-lg border border-slate-700 px-5 py-2.5 text-sm text-slate-200 transition hover:border-slate-500"
          >
            How customer discovery works
          </Link>
        </div>
      </section>
    </main>
  );
}
