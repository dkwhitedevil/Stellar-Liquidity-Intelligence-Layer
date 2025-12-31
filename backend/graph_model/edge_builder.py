from graph_model.graph_schema import GraphEdge
from graph_model.edge_aggregation import aggregate_signals


def build_edges(signals):
    """Aggregate signals and emit GraphEdge objects with per-edge summaries.

    - Aggregate signals per (src, dst, metric) and add aggregated attributes to edges.
    - For pair signals we create directed edges in both directions (with same aggregated summary).
    - For network-level signals we create a self-edge with aggregated summary.
    """
    edges = []

    summaries = aggregate_signals(signals)

    for (src, dst, metric), s in summaries.items():
        attrs = {
            "metric": metric,
            "agg_count": s["agg_count"],
            "agg_mean": s["agg_mean"],
            "agg_std": s["agg_std"],
            "agg_uncertainty": s["agg_uncertainty"],
            "last_ts": s["last_ts"].isoformat() if s["last_ts"] else None,
        }

        # Create edge with last_ts used as timestamp if available
        ts = s["last_ts"] if s["last_ts"] else None

        # For src==dst this naturally creates a self-edge; for pairs we keep directionality
        edges.append(GraphEdge(source=src, target=dst, timestamp=ts, attributes=attrs))

    return edges
