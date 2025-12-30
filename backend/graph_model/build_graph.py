from signal_processing.extract_all_signals import get_all_signals
from graph_model.node_builder import build_nodes
from graph_model.edge_builder import build_edges
from graph_model.temporal_graph import build_temporal_graph
from graph_model.graph_registry import validate_graph
from graph_model.graph_snapshot import save_graph_snapshot


if __name__ == "__main__":
    signals = get_all_signals()

    nodes = build_nodes(signals)
    edges = build_edges(signals)

    G = build_temporal_graph(nodes, edges)
    validate_graph(G)

    path = save_graph_snapshot(G)

    print(f"Phase 3 complete. Graph nodes={G.number_of_nodes()}, edges={G.number_of_edges()}")
    print(f"Snapshot saved at {path}")
