import networkx as nx


def enumerate_paths(G, source, destination, max_hops=3):
    # networkx cutoff is the maximum path length; convert hops to nodes cutoff
    cutoff = max_hops + 1
    try:
        return list(nx.all_simple_paths(G, source, destination, cutoff=cutoff))
    except Exception:
        return []
