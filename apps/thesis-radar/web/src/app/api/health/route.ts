import { NextResponse } from "next/server";

import { checkDatabase } from "@/lib/db";
import { checkHealth, isSignalEngineAvailable } from "@/lib/signal-engine";

export const dynamic = "force-dynamic";

export async function GET() {
  const [engineUp, database] = await Promise.all([
    isSignalEngineAvailable(),
    checkDatabase(),
  ]);
  const engine = engineUp ? await checkHealth() : null;

  return NextResponse.json({
    status: "ok",
    app: "thesis-radar-web",
    database: database.ok ? { status: "ok" } : { status: "unavailable", error: database.error },
    signalEngine: engine ?? { status: "unavailable" },
  });
}