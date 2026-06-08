import { NextResponse } from "next/server";

import { runPipelineDryRun } from "@/lib/signal-engine";

export const dynamic = "force-dynamic";

export async function POST() {
  try {
    const result = await runPipelineDryRun();
    return NextResponse.json(result);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Signal engine unavailable";
    return NextResponse.json({ error: message }, { status: 503 });
  }
}
