"""Tests for LangGraph pipeline structure."""

from signal_engine.graph.pipeline_graph import build_pipeline_graph


def test_pipeline_graph_has_expected_nodes() -> None:
    graph = build_pipeline_graph()
    node_names = set(graph.get_graph().nodes.keys())
    expected = {
        "__start__",
        "__end__",
        "load_thesis",
        "fetch_sources",
        "dedupe",
        "score_batch",
        "persist",
        "analyze_retention",
        "render_digest",
        "write_digest",
        "send_digest_email",
    }
    assert expected.issubset(node_names)
