from datetime import datetime, timedelta
from signal_processing.signal_schema import Signal
from graph_model.build_graph import build_temporal_graph
from graph_model.node_builder import build_nodes
from graph_model.edge_builder import build_edges
from graph_model.graph_snapshot import save_graph_snapshot

from fastapi.testclient import TestClient

from api.main import app


def generate_seeded_signals(n=50):
    now = datetime.utcnow()
    signals = []
    for i in range(n):
        ts = now - timedelta(minutes=i)
        # Alternate pair names to create a connected chain XLM->A -> B -> USDC
        base = f"A{i%5}"
        counter = f"B{(i+1)%5}"
        pair = f"{base}/{counter}"
        signals.append(Signal(ts, pair, "liquidity", "trade_volume", float(100 + i), "units", "trades"))
    # add final USDC connector
    signals.append(Signal(now, "A0/USDC", "liquidity", "trade_volume", 999.0, "units", "trades"))
    return signals


def test_e2e_build_and_paths(tmp_path, monkeypatch):
    signals = generate_seeded_signals(60)

    nodes = build_nodes(signals)
    edges = build_edges(signals)
    G = build_temporal_graph(nodes, edges)

    # Save snapshot to tmp dir and monkeypatch loader to return this graph
    p = tmp_path / "snap.gpickle"
    save_graph_snapshot(G, name="test_graph")

    # Monkeypatch load_latest_graph to return our graph G
    import graph_model.graph_snapshot as gs
    monkeypatch.setattr(gs, "load_latest_graph", lambda: G)

    client = TestClient(app)

    r = client.get('/graph/paths?from=A0&to=USDC')
    assert r.status_code == 200
    data = r.json()
    # Should be a list (possibly empty if policies filter, but should be valid response)
    assert isinstance(data, list)
