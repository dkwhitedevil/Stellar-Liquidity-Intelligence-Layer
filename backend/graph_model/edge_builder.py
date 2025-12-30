from graph_model.graph_schema import GraphEdge


def build_edges(signals):
    edges = []

    for s in signals:
        edges.append(
            GraphEdge(
                source=s.entity,
                target=s.entity,  # self-edge (temporal signal binding)
                timestamp=s.timestamp,
                attributes={
                    "dimension": s.dimension,
                    "metric": s.metric,
                    "value": s.value,
                    "unit": s.unit,
                    "source": s.source,
                }
            )
        )

    return edges
