"""Main pipeline CLI — delegates to LangGraph orchestration."""

from __future__ import annotations

import argparse
import asyncio
import logging
from pathlib import Path

from signal_engine.graph.pipeline_graph import run_pipeline_graph
from signal_engine.fetchers import fetch_hn, fetch_reddit
from signal_engine.models import RawSignal, ThesisConfig

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_THESIS = Path(__file__).resolve().parents[2] / "config" / "thesis_recruiting_ta.yaml"


async def fetch_all(thesis: ThesisConfig) -> list[RawSignal]:
    """Fetch from all sources (used by API dry-run)."""
    reddit_result, hn_result = await asyncio.gather(
        fetch_reddit(thesis),
        fetch_hn(thesis),
    )
    signals: list[RawSignal] = []
    seen: set[str] = set()
    for result in (reddit_result, hn_result):
        for signal in result.signals:
            key = f"{signal.source}:{signal.source_id}"
            if key not in seen:
                seen.add(key)
                signals.append(signal)
    return signals


async def run_pipeline(
    thesis_path: Path,
    *,
    dry_run: bool = False,
    skip_scoring: bool = False,
) -> Path:
    return await run_pipeline_graph(
        thesis_path,
        dry_run=dry_run,
        skip_scoring=skip_scoring,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the signal engine pipeline")
    parser.add_argument(
        "--thesis",
        type=Path,
        default=DEFAULT_THESIS,
        help="Path to thesis YAML config",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch only; skip LLM scoring and DB writes",
    )
    parser.add_argument(
        "--skip-scoring",
        action="store_true",
        help="Skip LLM scoring but still write empty digest",
    )
    args = parser.parse_args()
    asyncio.run(
        run_pipeline(
            args.thesis,
            dry_run=args.dry_run,
            skip_scoring=args.skip_scoring,
        )
    )


if __name__ == "__main__":
    main()
