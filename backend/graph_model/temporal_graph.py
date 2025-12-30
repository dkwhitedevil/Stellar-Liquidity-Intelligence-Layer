import networkx as nx
from graph_model.graph_schema import GraphNode, GraphEdge


def build_temporal_graph(nodes, edges):
    G = nx.MultiDiGraph()

    for node in nodes.values():
        G.add_node(
            node.node_id,
            node_type=node.node_type,
            metadata=node.metadata
        )

    for edge in edges:
        G.add_edge(
            edge.source,
            edge.target,
            timestamp=edge.timestamp,
            **edge.attributes
        )

    return G
