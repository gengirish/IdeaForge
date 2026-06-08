function required(name: string, value: string | undefined): string {
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

/** Server-only URL for the Python signal-engine API (FastAPI). */
export function getSignalEngineApiUrl(): string {
  return process.env.SIGNAL_ENGINE_API_URL ?? "http://localhost:8000";
}

/** Postgres connection string — used by future Prisma/Server Actions. */
export function getDatabaseUrl(): string {
  return required("DATABASE_URL", process.env.DATABASE_URL);
}
