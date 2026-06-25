import Image from "next/image";
import Link from "next/link";

const FOUNDER_LINKS = {
  portfolio: "https://founder.intelliforge.tech/",
  linkedin: "https://www.linkedin.com/in/girish-b-hiremath/",
  email: "mailto:gen.girish@gmail.com",
  github: "https://github.com/gengirish",
} as const;

const FOUNDER_HIGHLIGHTS = [
  "14+ years building enterprise software across compliance, banking, pharma, telecom, and IoT",
  "M.Tech in Data Science & AI at IIIT Dharwad — NLP, generative AI, RAG systems, LangChain",
  "Principal Software Engineer leading AI-powered compliance platforms and production LLM workflows",
  "Dogfooding ThesisRadar on real customer discovery — LangGraph pipelines, daily digest in production",
] as const;

function LinkedInIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
    </svg>
  );
}

export function FounderCard() {
  return (
    <article className="rounded-xl border border-slate-800 bg-slate-900/40 p-6">
      <div className="mb-6 flex flex-col gap-5 sm:flex-row sm:items-start">
        <Link
          href={FOUNDER_LINKS.portfolio}
          target="_blank"
          rel="noopener noreferrer"
          className="shrink-0 overflow-hidden rounded-xl border border-slate-700/80 ring-2 ring-brand-900/40 transition hover:border-slate-600 hover:ring-brand-700/50"
        >
          <Image
            src="/founder/girish-hiremath-portfolio.png"
            alt="Girish Hiremath — portfolio at founder.intelliforge.tech"
            width={200}
            height={105}
            className="h-auto w-full max-w-[12.5rem] object-cover sm:w-48"
            priority
          />
        </Link>
        <div className="min-w-0 flex-1">
          <h3 className="text-xl font-semibold text-slate-100">Girish Hiremath</h3>
          <p className="text-sm text-brand-400">Founder, IntelliForge · AI Practitioner</p>
          <p className="mt-1 text-sm text-slate-500">
            M.Tech Data Science &amp; AI — IIIT Dharwad · 14+ years enterprise software
          </p>
        </div>
      </div>
      <p className="mb-6 text-sm leading-relaxed text-slate-300">
        AI practitioner and full-stack architect with 14+ years across compliance, banking, pharma,
        telecom, and IoT — from early neural-network experiments at a semiconductor company to
        leading AI-powered compliance platforms today. Pursuing an M.Tech in Data Science &amp; AI
        at IIIT Dharwad while building IntelliForge products: ThesisRadar for founder customer
        discovery and Vettd for AI interviews. The thesis: the best discovery tools are built by
        engineers who understand both the algorithms and the real-world systems they serve.
      </p>
      <ul className="mb-6 grid gap-2 sm:grid-cols-2">
        {FOUNDER_HIGHLIGHTS.map((item) => (
          <li key={item} className="flex gap-2 text-sm text-slate-400">
            <span className="shrink-0 text-brand-500" aria-hidden>
              ·
            </span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
      <div className="flex flex-wrap gap-3">
        <a
          href={FOUNDER_LINKS.portfolio}
          target="_blank"
          rel="noopener noreferrer"
          className="rounded-lg bg-brand-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-brand-700"
        >
          Full portfolio →
        </a>
        <a
          href={FOUNDER_LINKS.linkedin}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-200 transition hover:border-slate-500"
        >
          <LinkedInIcon className="h-4 w-4 text-[#0A66C2]" />
          LinkedIn
        </a>
        <a
          href={FOUNDER_LINKS.email}
          className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-200 transition hover:border-slate-500"
        >
          gen.girish@gmail.com
        </a>
      </div>
    </article>
  );
}
