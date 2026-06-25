import "server-only";

import { neon } from "@neondatabase/serverless";

import type { DigestSampleSignal } from "@/components/digest-sample-card";

export type PipelineRunStats = {
  thesisName: string;
  thesisVertical: string;
  signalsScored: number;
  interviewWorthy: number;
  prefilterFrom: number;
  prefilterTo: number;
  completedAt: string;
};

export type PipelineCorpusStats = {
  totalSignals: number;
  totalInterviewWorthy: number;
  runsLast24h: number;
  latestRun: PipelineRunStats | null;
};

const FALLBACK_RUN: PipelineRunStats = {
  thesisName: "field_service_hvac",
  thesisVertical: "Field Service — HVAC",
  signalsScored: 30,
  interviewWorthy: 5,
  prefilterFrom: 567,
  prefilterTo: 30,
  completedAt: "2026-06-09T12:25:00.000Z",
};

const FALLBACK_SAMPLES: DigestSampleSignal[] = [
  {
    title: "Request: Field Service + CRM + Product Sales + Project Management all-in-one?",
    url: "https://reddit.com/r/smallbusiness/comments/lmy390/request_field_service_crm_product_sales_project/",
    source: "reddit",
    urgency: 4,
    scorecard:
      "pain=Y, freq=monthly, paying=Y, persona=buyer, would_pay=maybe, thesis=supports",
    rationale:
      "The author describes using multiple software tools for sales, CRM, project management, and field service scheduling, indicating real pain from inefficiency and a willingness to streamline.",
  },
  {
    title: "In need of a scheduling/dispatch software that works well!",
    url: "https://reddit.com/r/HVAC/comments/1hhy7hz/in_need_of_a_schedulingdispatch_software_that/",
    source: "reddit",
    urgency: 4,
    scorecard:
      "pain=Y, freq=monthly, paying=Y, persona=champion, would_pay=maybe, thesis=supports",
    rationale:
      "The author describes a specific pain point with their current scheduling system (House Call Pro) and manual Excel spreadsheet, and is seeking a more efficient solution.",
  },
  {
    title: "Service/Repair Plumbers - how do you organize day-to-day operations?",
    url: "https://reddit.com/r/Plumbing/comments/frkd6y/servicerepair_plumbers_how_do_you_organize/",
    source: "reddit",
    urgency: 4,
    scorecard:
      "pain=Y, freq=weekly, paying=N, persona=champion, would_pay=maybe, thesis=supports",
    rationale:
      "The author describes a specific instance of their current inefficient scheduling process causing stress and inefficiency, and is actively researching solutions.",
  },
];

type LatestRunRow = {
  thesis_name: string;
  thesis_vertical: string;
  scored_count: number;
  interview_worthy_count: number;
  deduped_count: number;
  prefilter_skipped: number;
  completed_at: Date;
};

type SignalRow = {
  title: string;
  url: string;
  source: string;
  urgency: number;
  pain_real: string;
  pain_frequency: string;
  already_paying: string;
  persona_fit: string;
  would_pay: string;
  thesis_fit: string;
  rationale: string;
};

function getDatabaseUrl(): string | undefined {
  return process.env.DATABASE_URL;
}

function formatScorecard(row: SignalRow): string {
  return [
    `pain=${row.pain_real}`,
    `freq=${row.pain_frequency}`,
    `paying=${row.already_paying}`,
    `persona=${row.persona_fit}`,
    `would_pay=${row.would_pay}`,
    `thesis=${row.thesis_fit}`,
  ].join(", ");
}

function mapLatestRun(row: LatestRunRow): PipelineRunStats {
  const prefilterFrom = row.deduped_count + row.prefilter_skipped;
  return {
    thesisName: row.thesis_name,
    thesisVertical: row.thesis_vertical,
    signalsScored: row.scored_count,
    interviewWorthy: row.interview_worthy_count,
    prefilterFrom,
    prefilterTo: row.scored_count,
    completedAt: row.completed_at.toISOString(),
  };
}

function mapSignalRow(row: SignalRow): DigestSampleSignal {
  return {
    title: row.title,
    url: row.url,
    source: row.source,
    urgency: row.urgency,
    scorecard: formatScorecard(row),
    rationale: row.rationale,
  };
}

export async function getPipelineCorpusStats(): Promise<{
  stats: PipelineCorpusStats;
  source: "live" | "fallback";
}> {
  const databaseUrl = getDatabaseUrl();
  if (!databaseUrl) {
    return {
      stats: {
        totalSignals: 0,
        totalInterviewWorthy: FALLBACK_RUN.interviewWorthy,
        runsLast24h: 0,
        latestRun: FALLBACK_RUN,
      },
      source: "fallback",
    };
  }

  try {
    const sql = neon(databaseUrl);

    const [latestRows, corpusRows, runsRows] = await Promise.all([
      sql`
        SELECT thesis_name, thesis_vertical, scored_count, interview_worthy_count,
               deduped_count, prefilter_skipped, completed_at
        FROM pipeline_runs
        ORDER BY completed_at DESC
        LIMIT 1
      `,
      sql`
        SELECT
          (SELECT COUNT(*)::int FROM signals) AS total_signals,
          (SELECT COUNT(*)::int FROM scorecards WHERE interview_worthy = TRUE) AS total_interview_worthy
      `,
      sql`
        SELECT COUNT(*)::int AS runs_last_24h
        FROM pipeline_runs
        WHERE completed_at > NOW() - INTERVAL '24 hours'
      `,
    ]);

    const latestRow = latestRows[0] as LatestRunRow | undefined;
    const corpusRow = corpusRows[0] as
      | { total_signals: number; total_interview_worthy: number }
      | undefined;
    const runsRow = runsRows[0] as { runs_last_24h: number } | undefined;

    if (!latestRow) {
      return {
        stats: {
          totalSignals: 0,
          totalInterviewWorthy: 0,
          runsLast24h: 0,
          latestRun: null,
        },
        source: "fallback",
      };
    }

    return {
      stats: {
        totalSignals: corpusRow?.total_signals ?? 0,
        totalInterviewWorthy: corpusRow?.total_interview_worthy ?? 0,
        runsLast24h: runsRow?.runs_last_24h ?? 0,
        latestRun: mapLatestRun(latestRow),
      },
      source: "live",
    };
  } catch {
    return {
      stats: {
        totalSignals: 0,
        totalInterviewWorthy: FALLBACK_RUN.interviewWorthy,
        runsLast24h: 0,
        latestRun: FALLBACK_RUN,
      },
      source: "fallback",
    };
  }
}

export async function getInterviewWorthySamples(
  limit = 3,
): Promise<{ signals: DigestSampleSignal[]; source: "live" | "fallback" }> {
  const databaseUrl = getDatabaseUrl();
  if (!databaseUrl) {
    return { signals: FALLBACK_SAMPLES.slice(0, limit), source: "fallback" };
  }

  try {
    const sql = neon(databaseUrl);
    const rows = await sql`
      SELECT s.title, s.url, s.source, sc.urgency, sc.pain_real, sc.pain_frequency,
             sc.already_paying, sc.persona_fit, sc.would_pay, sc.thesis_fit, sc.rationale
      FROM signals s
      INNER JOIN scorecards sc ON sc.signal_id = s.id
      WHERE sc.interview_worthy = TRUE
      ORDER BY sc.scored_at DESC
      LIMIT ${limit}
    `;

    if (rows.length === 0) {
      return { signals: FALLBACK_SAMPLES.slice(0, limit), source: "fallback" };
    }

    return {
      signals: (rows as SignalRow[]).map(mapSignalRow),
      source: "live",
    };
  } catch {
    return { signals: FALLBACK_SAMPLES.slice(0, limit), source: "fallback" };
  }
}

export function formatRunDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  });
}
