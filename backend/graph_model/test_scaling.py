import time
from datetime import datetime, timedelta
from signal_processing.signal_schema import Signal
from graph_model.node_builder import build_nodes
from graph_model.edge_builder import build_edges
from graph_model.temporal_graph import build_temporal_graph


def generate_many_signals(n=1000):
    now = datetime.utcnow()
    signals = []
    for i in range(n):
        ts = now - timedelta(seconds=i)
        base = f"X{i%50}"
        counter = f"Y{(i+1)%50}"
        pair = f"{base}/{counter}"
        signals.append(Signal(ts, pair, "liquidity", "trade_volume", float(i%100), "units", "trades"))
    return signals


def test_build_time_is_reasonable():
    signals = generate_many_signals(1000)
    t0 = time.perf_counter()
    nodes = build_nodes(signals)
    edges = build_edges(signals)
    G = build_temporal_graph(nodes, edges)
    elapsed = time.perf_counter() - t0
    print(f"build time for 1000 signals: {elapsed:.3f}s, nodes={G.number_of_nodes()}, edges={G.number_of_edges()}")
    assert G.number_of_edges() > 0
    # Make sure build finishes in a reasonable time on CI; allow up to 5s
    assert elapsed < 5.0
