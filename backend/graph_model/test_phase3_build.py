from datetime import datetime

from signal_processing.signal_schema import Signal
from graph_model.node_builder import build_nodes
from graph_model.edge_builder import build_edges
from graph_model.temporal_graph import build_temporal_graph


def test_build_temporal_graph_from_signals():
    now = datetime.utcnow()

    signals = [
        Signal(now, "XLM/USDC", "activity", "trade_count", 10.0, "count", "trades"),
        Signal(now, "XLM/USDC", "liquidity", "trade_volume", 500.0, "units", "trades"),
        Signal(now, "NETWORK", "flow", "payment_count", 5.0, "count", "payments"),
    ]

    nodes = build_nodes(signals)
    assert "XLM" in nodes and "USDC" in nodes

    edges = build_edges(signals)
    assert any(e.source == "XLM" and e.target == "USDC" for e in edges)
    assert any(e.source == "USDC" and e.target == "XLM" for e in edges)

    G = build_temporal_graph(nodes, edges)
    assert G.number_of_nodes() >= 3
    assert G.number_of_edges() >= 2
