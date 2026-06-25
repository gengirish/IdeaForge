import type { Metadata } from "next";
import Link from "next/link";

import { DigestSampleCard } from "@/components/digest-sample-card";
import { PipelineStatsBanner } from "@/components/pipeline-stats-banner";
import {
  formatRunDate,
  getInterviewWorthySamples,
  getPipelineCorpusStats,
} from "@/lib/pipeline-stats";

export const metadata: Metadata = {
  title: "Digest examples — ThesisRadar",
  description:
    "See what a daily ThesisRadar digest looks like — interview-worthy signals with scorecards, source receipts, and thesis fit.",
};

export const revalidate = 300;

const gateCriteria = [
  { label: "Pain real?", detail: "Specific past instance, not vague annoyance" },
  { label: "Buyer or champion", detail: "Persona fit — not user-only or disqualifier" },
  { label: "Would pay", detail: "Y or maybe — willingness to switch or adopt" },
  { label: "Urgency ≥ 3", detail: "Active problem, not idle curiosity" },
  { label: "Thesis supports", detail: "Signal aligns with your ICP + JTBD bet" },
];

export default async function ExamplesPage() {
  const [{ stats, source: statsSource }, { signals, source: signalsSource }] =
    await Promise.all([getPipelineCorpusStats(), getInterviewWorthySamples(3)]);

  const run = stats.latestRun;
  const displayRun = run ?? {
    thesisName: "sample",
    thesisVertical: "Field Service — HVAC",
    signalsScored: 30,
    interviewWorthy: 5,
    prefilterFrom: 567,
    prefilterTo: 30,
    completedAt: "2026-06-09T12:25:00.000Z",
  };

  const dataSource =
    statsSource === "live" || signalsSource === "live" ? "live" : "fallback";

  return (
    <main className="mx-auto max-w-4xl px-6 py-16">
      <header className="mb-12">
        <p className="mb-2 text-sm font-medium uppercase tracking-widest text-brand-500">
          Sample digest
        </p>
        <h1 className="mb-4 text-4xl font-bold tracking-tight sm:text-5xl">
          See what a daily digest looks like
        </h1>
        <p className="max-w-2xl text-lg text-slate-400">
          {dataSource === "live"
            ? "Live interview-worthy signals from the production corpus — scored against active theses and filtered to discovery-call quality."
            : "Sample signals from a production pipeline run — scored against a Field Service HVAC thesis, filtered from hundreds of posts to the few worth a discovery call."}
        </p>
      </header>

      <div className="mb-12">
        <PipelineStatsBanner
          run={displayRun}
          source={statsSource}
          runsLast24h={stats.runsLast24h}
          totalSignals={stats.totalSignals}
        />
      </div>

      <section className="mb-12">
        <h2 className="mb-6 text-2xl font-semibold">Interview-worthy signals</h2>
        <div className="grid gap-4">
          {signals.map((signal) => (
            <DigestSampleCard key={signal.url} signal={signal} />
          ))}
        </div>
      </section>

      <section className="mb-12">
        <h2 className="mb-2 text-2xl font-semibold">Why these passed the gate</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Signals only surface for outreach when they pass evidence thresholds — not when an LLM
          feels optimistic. Each dimension is scored with linked source receipts.
        </p>
        <ul className="grid gap-3 sm:grid-cols-2">
          {gateCriteria.map((field) => (
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

      <p className="mb-12 text-sm text-slate-500">
        {dataSource === "live"
          ? `Pulled from production Postgres · last pipeline run ${formatRunDate(displayRun.completedAt)}. Full digests delivered daily to founding members.`
          : `Sample from production pipeline run, ${formatRunDate(displayRun.completedAt)}. Full digests delivered daily to founding members.`}
      </p>

      <section className="rounded-xl border border-brand-900/50 bg-brand-900/10 p-6 sm:p-8">
        <h2 className="mb-2 text-2xl font-semibold">Get your own daily digest</h2>
        <p className="mb-6 max-w-2xl text-slate-400">
          Define your thesis once. Wake up to scored signals with source receipts — and know who to
          interview next.
        </p>
        <Link
          href="/sign-up"
          className="inline-flex rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-brand-700"
        >
          Start founding member access
        </Link>
      </section>
    </main>
  );
}
