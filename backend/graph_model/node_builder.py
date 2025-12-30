from signal_processing.signal_schema import Signal
from graph_model.graph_schema import GraphNode


def build_nodes(signals):
    nodes = {}

    for s in signals:
        if s.entity not in nodes:
            nodes[s.entity] = GraphNode(
                node_id=s.entity,
                node_type="asset_pair" if "/" in s.entity else "network",
                metadata={}
            )

    return nodes
