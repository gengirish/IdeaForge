import "server-only";

import { neon } from "@neondatabase/serverless";

import { getDatabaseUrl } from "@/lib/env";

export async function checkDatabase(): Promise<{ ok: true } | { ok: false; error: string }> {
  try {
    const sql = neon(getDatabaseUrl());
    await sql`SELECT 1 AS ok`;
    return { ok: true };
  } catch (err) {
    const message = err instanceof Error ? err.message : "Database unavailable";
    return { ok: false, error: message };
  }
}
