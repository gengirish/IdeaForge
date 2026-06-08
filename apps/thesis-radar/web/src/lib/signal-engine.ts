import "server-only";

import { getSignalEngineApiUrl } from "@/lib/env";
import type { DryRunResponse, HealthResponse, ThesisConfig } from "@/types/signal";

const BASE = () => getSignalEngineApiUrl();

async function engineFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE()}${path}`, {
    ...init,
    cache: "no-store",
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`Signal engine ${path} failed (${res.status}): ${detail}`);
  }

  return res.json() as Promise<T>;
}

export async function checkHealth(): Promise<HealthResponse> {
  return engineFetch<HealthResponse>("/health");
}

export async function getDefaultThesis(): Promise<ThesisConfig> {
  return engineFetch<ThesisConfig>("/v1/thesis/default");
}

export async function runPipelineDryRun(): Promise<DryRunResponse> {
  return engineFetch<DryRunResponse>("/v1/pipeline/dry-run", { method: "POST" });
}

export async function isSignalEngineAvailable(): Promise<boolean> {
  try {
    await checkHealth();
    return true;
  } catch {
    return false;
  }
}
