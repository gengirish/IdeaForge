import { SignalPreview } from "@/components/signal-preview";
import { runPipelineDryRun } from "@/lib/signal-engine";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  let dryRun = null;
  try {
    dryRun = await runPipelineDryRun();
  } catch {
    dryRun = null;
  }

  return (
    <main className="mx-auto max-w-4xl px-6 py-16">
      <header className="mb-12">
        <p className="mb-2 text-sm font-medium uppercase tracking-widest text-brand-500">
          Signal Engine / ThesisRadar
        </p>
        <h1 className="mb-4 text-4xl font-bold tracking-tight">
          Daily evidence for founders with a bet
        </h1>
        <p className="max-w-2xl text-lg text-slate-400">
          Not idea tourists — thesis-driven, evidence-grade signals that answer: is this problem
          hair-on-fire for your ICP, and who do you talk to next?
        </p>
      </header>

      <section className="mb-10 grid gap-4 sm:grid-cols-3">
        {[
          { label: "Architecture", value: "Next.js fullstack" },
          { label: "Vertical", value: "Recruiting / TA" },
          { label: "Pricing (Phase 1)", value: "$49/mo founding" },
        ].map((item) => (
          <div key={item.label} className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
            <p className="text-xs uppercase text-slate-500">{item.label}</p>
            <p className="mt-1 font-medium">{item.value}</p>
          </div>
        ))}
      </section>

      <section className="rounded-xl border border-slate-800 bg-slate-900/30 p-6">
        <h2 className="mb-2 text-xl font-semibold">Live signal preview</h2>
        <p className="mb-4 text-sm text-slate-400">
          Server-rendered via Next.js → Python signal engine (Reddit + HN dry-run). Full scoring
          runs in <code className="rounded bg-slate-800 px-1">signal-engine</code>.
        </p>
        <SignalPreview dryRun={dryRun} />
      </section>

      <footer className="mt-12 text-sm text-slate-500">
        Phase 1: thesis wizard · scorecard · Stripe · Resend digest · waitlist
      </footer>
    </main>
  );
}
