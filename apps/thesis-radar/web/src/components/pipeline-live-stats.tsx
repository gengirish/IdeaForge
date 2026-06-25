import { getPipelineCorpusStats } from "@/lib/pipeline-stats";

export async function PipelineLiveStats() {
  const { stats, source } = await getPipelineCorpusStats();
  const run = stats.latestRun;

  if (!run) {
    return (
      <p className="mb-8 text-sm text-slate-500">
        Pipeline telemetry will appear after the first scheduled run writes to Postgres.
      </p>
    );
  }

  return (
    <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {[
        {
          label: "Latest run scored",
          value: String(run.signalsScored),
          detail: `${run.interviewWorthy} interview-worthy`,
        },
        {
          label: "Corpus size",
          value: stats.totalSignals > 0 ? String(stats.totalSignals) : "—",
          detail: `${stats.totalInterviewWorthy} interview-worthy total`,
        },
        {
          label: "Runs (24h)",
          value: stats.runsLast24h > 0 ? String(stats.runsLast24h) : "—",
          detail: "Scheduled every 4h",
        },
        {
          label: "Latest thesis",
          value: run.thesisVertical,
          detail: source === "live" ? "Live from Postgres" : "Archived sample",
        },
      ].map((item) => (
        <article
          key={item.label}
          className="rounded-xl border border-brand-900/40 bg-brand-900/10 p-5"
        >
          <p className="text-xs uppercase tracking-wide text-slate-500">{item.label}</p>
          <p className="mt-2 font-semibold text-slate-100">{item.value}</p>
          <p className="mt-1 text-sm text-slate-400">{item.detail}</p>
        </article>
      ))}
    </div>
  );
}
