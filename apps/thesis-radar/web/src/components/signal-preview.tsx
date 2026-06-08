import type { DryRunResponse } from "@/types/signal";

interface SignalPreviewProps {
  dryRun: DryRunResponse | null;
}

export function SignalPreview({ dryRun }: SignalPreviewProps) {
  if (!dryRun) {
    return (
      <p className="text-amber-400">
        Signal engine unavailable — start the Python API with{" "}
        <code className="rounded bg-slate-800 px-1">
          cd apps/thesis-radar/api && uv run uvicorn thesis_radar_api.main:app --reload
        </code>
      </p>
    );
  }

  return (
    <>
      <p className="mb-4 text-sm text-slate-300">{dryRun.count} signals fetched</p>
      <ul className="space-y-3">
        {dryRun.signals.slice(0, 8).map((s) => (
          <li key={s.url} className="rounded-lg border border-slate-800 p-3">
            <span className="mr-2 rounded bg-brand-900/50 px-2 py-0.5 text-xs text-brand-500">
              {s.source}
            </span>
            <a
              href={s.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-200 hover:text-white hover:underline"
            >
              {s.title}
            </a>
          </li>
        ))}
      </ul>
    </>
  );
}
