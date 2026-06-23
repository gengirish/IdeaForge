import type { Metadata } from "next";
import Link from "next/link";

import { DigestSampleCard, type DigestSampleSignal } from "@/components/digest-sample-card";

export const metadata: Metadata = {
  title: "Digest examples — ThesisRadar",
  description:
    "See what a daily ThesisRadar digest looks like — interview-worthy signals with scorecards, source receipts, and thesis fit.",
};

const pipelineStats = {
  signalsScored: 30,
  interviewWorthy: 5,
  prefilterFrom: 567,
  prefilterTo: 30,
  thesis: "Field Service — HVAC",
};

const sampleSignals: DigestSampleSignal[] = [
  {
    title: "Request: Field Service + CRM + Product Sales + Project Management all-in-one?",
    url: "https://reddit.com/r/smallbusiness/comments/lmy390/request_field_service_crm_product_sales_project/",
    source: "reddit",
    urgency: 4,
    scorecard:
      "pain=Y, freq=monthly, paying=Y, persona=buyer, would_pay=maybe, thesis=supports",
    rationale:
      "The author describes using multiple software tools for sales, CRM, project management, and field service scheduling, indicating real pain from inefficiency and a willingness to streamline.",
  },
  {
    title: "In need of a scheduling/dispatch software that works well!",
    url: "https://reddit.com/r/HVAC/comments/1hhy7hz/in_need_of_a_schedulingdispatch_software_that/",
    source: "reddit",
    urgency: 4,
    scorecard:
      "pain=Y, freq=monthly, paying=Y, persona=champion, would_pay=maybe, thesis=supports",
    rationale:
      "The author describes a specific pain point with their current scheduling system (House Call Pro) and manual Excel spreadsheet, and is seeking a more efficient solution.",
  },
  {
    title: "Service/Repair Plumbers - how do you organize day-to-day operations?",
    url: "https://reddit.com/r/Plumbing/comments/frkd6y/servicerepair_plumbers_how_do_you_organize/",
    source: "reddit",
    urgency: 4,
    scorecard:
      "pain=Y, freq=weekly, paying=N, persona=champion, would_pay=maybe, thesis=supports",
    rationale:
      "The author describes a specific instance of their current inefficient scheduling process causing stress and inefficiency, and is actively researching solutions.",
  },
];

const gateCriteria = [
  { label: "Pain real?", detail: "Specific past instance, not vague annoyance" },
  { label: "Buyer or champion", detail: "Persona fit — not user-only or disqualifier" },
  { label: "Would pay", detail: "Y or maybe — willingness to switch or adopt" },
  { label: "Urgency ≥ 3", detail: "Active problem, not idle curiosity" },
  { label: "Thesis supports", detail: "Signal aligns with your ICP + JTBD bet" },
];

export default function ExamplesPage() {
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
          Real signals from a production pipeline run — scored against a Field Service HVAC thesis,
          filtered from hundreds of posts to the few worth a discovery call.
        </p>
      </header>

      <section
        className="mb-12 rounded-xl border border-slate-800 bg-slate-900/30 p-5 sm:p-6"
        aria-label="Pipeline stats"
      >
        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-500">Signals scored</dt>
            <dd className="mt-1 text-2xl font-semibold text-slate-100">
              {pipelineStats.signalsScored}
            </dd>
          </div>
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-500">Interview-worthy</dt>
            <dd className="mt-1 text-2xl font-semibold text-brand-400">
              {pipelineStats.interviewWorthy}
            </dd>
          </div>
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-500">Prefilter</dt>
            <dd className="mt-1 text-2xl font-semibold text-slate-100">
              {pipelineStats.prefilterFrom}→{pipelineStats.prefilterTo}
            </dd>
          </div>
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-500">Thesis</dt>
            <dd className="mt-1 text-lg font-semibold text-slate-100">{pipelineStats.thesis}</dd>
          </div>
        </dl>
      </section>

      <section className="mb-12">
        <h2 className="mb-6 text-2xl font-semibold">Interview-worthy signals</h2>
        <div className="grid gap-4">
          {sampleSignals.map((signal) => (
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
        Sample from production pipeline run, 2026-06-09. Full digests delivered daily to founding
        members.
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
