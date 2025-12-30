import networkx as nx
from pathlib import Path
from datetime import datetime


def save_graph_snapshot(G, name="graph"):
    out = Path("graph_snapshots")
    out.mkdir(exist_ok=True)

    ts = datetime.utcnow().isoformat()
    path = out / f"{name}_{ts}.gpickle"

    # Use the gpickle writer from networkx.readwrite for compatibility across nx versions
    # Try various ways to write a gpickle to be compatible across environments
    try:
        import networkx.readwrite.gpickle as gpickle
        gpickle.write_gpickle(G, path)
        return path
    except Exception:
        pass

    try:
        if hasattr(nx, "write_gpickle"):
            nx.write_gpickle(G, path)
            return path
    except Exception:
        pass

    # Last-resort fallback: use pickle directly
    import pickle
    with open(path, "wb") as f:
        pickle.dump(G, f)

    return path
