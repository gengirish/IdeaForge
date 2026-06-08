import { currentUser } from "@clerk/nextjs/server";

import { SignalPreview } from "@/components/signal-preview";
import { runPipelineDryRun } from "@/lib/signal-engine";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const user = await currentUser();
  let dryRun = null;
  try {
    dryRun = await runPipelineDryRun();
  } catch {
    dryRun = null;
  }

  return (
    <main className="mx-auto max-w-4xl px-6 py-16">
      <header className="mb-10">
        <p className="mb-2 text-sm font-medium uppercase tracking-widest text-brand-500">
          Your workspace
        </p>
        <h1 className="mb-2 text-3xl font-bold tracking-tight">
          Welcome{user?.firstName ? `, ${user.firstName}` : ""}
        </h1>
        <p className="text-slate-400">
          Thesis-driven signals for your active bet — interview-worthy evidence, not idea tourism.
        </p>
      </header>

      <section className="rounded-xl border border-slate-800 bg-slate-900/30 p-6">
        <h2 className="mb-2 text-xl font-semibold">Live signal preview</h2>
        <p className="mb-4 text-sm text-slate-400">
          Fetched server-side from the signal engine (Reddit + HN dry-run).
        </p>
        <SignalPreview dryRun={dryRun} />
      </section>
    </main>
  );
}
