import Link from "next/link";

export type DigestSampleSignal = {
  title: string;
  url: string;
  source: string;
  urgency: number;
  scorecard: string;
  rationale: string;
};

type DigestSampleCardProps = {
  signal: DigestSampleSignal;
};

export function DigestSampleCard({ signal }: DigestSampleCardProps) {
  return (
    <article className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
      <div className="mb-3 flex flex-wrap items-start justify-between gap-2">
        <h3 className="text-base font-semibold leading-snug text-slate-100">
          <Link
            href={signal.url}
            target="_blank"
            rel="noopener noreferrer"
            className="transition hover:text-brand-400"
          >
            {signal.title}
          </Link>
        </h3>
        <span className="shrink-0 rounded-full border border-brand-800/60 bg-brand-900/40 px-2.5 py-0.5 text-xs font-medium text-brand-400">
          Interview-worthy
        </span>
      </div>
      <p className="mb-3 text-sm text-slate-500">
        Source: {signal.source} · Urgency: {signal.urgency}/5
      </p>
      <p className="mb-3 font-mono text-xs text-slate-400">{signal.scorecard}</p>
      <p className="line-clamp-3 text-sm text-slate-300">{signal.rationale}</p>
    </article>
  );
}
