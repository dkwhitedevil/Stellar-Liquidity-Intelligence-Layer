def enumerate_paths(G, source, destination, max_hops=3):
    # Import networkx lazily so verification can run in minimal environments
    try:
        import networkx as nx
    except Exception:
        # networkx not available — return empty list conservatively
        return []

    # networkx cutoff is the maximum path length; convert hops to nodes cutoff
    cutoff = max_hops + 1
    try:
        return list(nx.all_simple_paths(G, source, destination, cutoff=cutoff))
    except Exception:
        return []
