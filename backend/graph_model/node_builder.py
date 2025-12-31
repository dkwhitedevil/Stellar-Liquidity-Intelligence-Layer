from signal_processing.signal_schema import Signal
from graph_model.graph_schema import GraphNode


def build_nodes(signals):
    """Build a mapping of node_id -> GraphNode.

    - For pair entities like "BASE/COUNTER" we create individual asset nodes for BASE and COUNTER
      with node_type 'asset'.
    - For other entity types (e.g., "NETWORK" or "ORDERBOOK") we create a network node.
    """
    nodes = {}

    for s in signals:
        # Asset pair signals (e.g., "XLM/USDC") should yield separate asset nodes
        if "/" in s.entity:
            base, counter = s.entity.split("/", 1)
            for asset in (base, counter):
                if asset not in nodes:
                    nodes[asset] = GraphNode(
                        node_id=asset,
                        node_type="asset",
                        metadata={}
                    )
        else:
            # Generic network-like entities (NETWORK, ORDERBOOK, etc.)
            if s.entity not in nodes:
                nodes[s.entity] = GraphNode(
                    node_id=s.entity,
                    node_type="network",
                    metadata={}
                )

    return nodes
