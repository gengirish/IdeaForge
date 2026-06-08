"""LangGraph StateGraph for fetch → dedupe → score → persist → digest."""

from __future__ import annotations

from pathlib import Path

from langgraph.graph import END, START, StateGraph

from signal_engine.graph.nodes import (
    node_analyze_retention,
    node_dedupe,
    node_fetch_sources,
    node_load_thesis,
    node_persist,
    node_render_digest,
    node_score_batch,
    node_send_digest_email,
    node_write_digest,
    route_after_dedupe,
)
from signal_engine.graph.state import PipelineState
from signal_engine.tracing import configure_tracing


def build_pipeline_graph():
    """Compile the daily signal pipeline graph."""
    builder = StateGraph(PipelineState)

    builder.add_node("load_thesis", node_load_thesis)
    builder.add_node("fetch_sources", node_fetch_sources)
    builder.add_node("dedupe", node_dedupe)
    builder.add_node("score_batch", node_score_batch)
    builder.add_node("persist", node_persist)
    builder.add_node("analyze_retention", node_analyze_retention)
    builder.add_node("render_digest", node_render_digest)
    builder.add_node("write_digest", node_write_digest)
    builder.add_node("send_digest_email", node_send_digest_email)

    builder.add_edge(START, "load_thesis")
    builder.add_edge("load_thesis", "fetch_sources")
    builder.add_edge("fetch_sources", "dedupe")
    builder.add_conditional_edges(
        "dedupe",
        route_after_dedupe,
        {"score_batch": "score_batch", "render_digest": "render_digest"},
    )
    builder.add_edge("score_batch", "persist")
    builder.add_edge("persist", "analyze_retention")
    builder.add_edge("analyze_retention", "render_digest")
    builder.add_edge("render_digest", "write_digest")
    builder.add_edge("write_digest", "send_digest_email")
    builder.add_edge("send_digest_email", END)

    return builder.compile()


async def run_pipeline_graph(
    thesis_path: Path,
    *,
    dry_run: bool = False,
    skip_scoring: bool = False,
) -> Path:
    configure_tracing()
    graph = build_pipeline_graph()
    result = await graph.ainvoke(
        {
            "thesis_path": str(thesis_path),
            "dry_run": dry_run,
            "skip_scoring": skip_scoring,
            "raw_signals": [],
            "scored_signals": [],
            "errors": [],
        }
    )
    digest_path = result.get("digest_path")
    if not digest_path:
        raise RuntimeError(f"Pipeline finished without digest path. State: {result}")
    return Path(digest_path)
