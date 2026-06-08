import { NextResponse } from "next/server";

import { getDefaultThesis } from "@/lib/signal-engine";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const thesis = await getDefaultThesis();
    return NextResponse.json(thesis);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Signal engine unavailable";
    return NextResponse.json({ error: message }, { status: 503 });
  }
}
