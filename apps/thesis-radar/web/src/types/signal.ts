export interface SignalSummary {
  source: string;
  title: string;
  url: string;
}

export interface DryRunResponse {
  count: number;
  signals: SignalSummary[];
}

export interface HealthResponse {
  status: string;
  version: string;
}

export type ThesisConfig = Record<string, unknown>;
