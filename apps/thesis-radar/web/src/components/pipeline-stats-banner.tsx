import type { PipelineRunStats } from "@/lib/pipeline-stats";
import { formatRunDate } from "@/lib/pipeline-stats";

type PipelineStatsBannerProps = {
  run: PipelineRunStats;
  source: "live" | "fallback";
  runsLast24h?: number;
  totalSignals?: number;
};

export function PipelineStatsBanner({
  run,
  source,
  runsLast24h,
  totalSignals,
}: PipelineStatsBannerProps) {
  return (
    <section
      className="rounded-xl border border-slate-800 bg-slate-900/30 p-5 sm:p-6"
      aria-label="Pipeline stats"
    >
      <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <dt className="text-xs uppercase tracking-wide text-slate-500">Signals scored</dt>
          <dd className="mt-1 text-2xl font-semibold text-slate-100">{run.signalsScored}</dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-wide text-slate-500">Interview-worthy</dt>
          <dd className="mt-1 text-2xl font-semibold text-brand-400">{run.interviewWorthy}</dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-wide text-slate-500">Prefilter</dt>
          <dd className="mt-1 text-2xl font-semibold text-slate-100">
            {run.prefilterFrom}→{run.prefilterTo}
          </dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-wide text-slate-500">Thesis</dt>
          <dd className="mt-1 text-lg font-semibold text-slate-100">{run.thesisVertical}</dd>
        </div>
      </dl>
      <p className="mt-4 text-xs text-slate-500">
        {source === "live" ? "Live from Postgres" : "Sample from archived digest"} · last run{" "}
        {formatRunDate(run.completedAt)}
        {runsLast24h !== undefined && runsLast24h > 0 ? ` · ${runsLast24h} runs in 24h` : ""}
        {totalSignals !== undefined && totalSignals > 0 ? ` · ${totalSignals} signals in corpus` : ""}
      </p>
    </section>
  );
}
