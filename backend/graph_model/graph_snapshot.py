from pathlib import Path
from datetime import datetime


def save_graph_snapshot(G, name="graph"):
    out = Path("graph_snapshots")
    out.mkdir(exist_ok=True)

    ts = datetime.utcnow().isoformat()
    path = out / f"{name}_{ts}.gpickle"

    # Use the gpickle writer from networkx.readwrite for compatibility across nx versions
    # Try to import networkx lazily to avoid hard dependency during verification
    try:
        import networkx.readwrite.gpickle as gpickle
        gpickle.write_gpickle(G, path)
        return path
    except Exception:
        pass

    try:
        import networkx as nx
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


def load_latest_graph():
    out = Path("graph_snapshots")
    if not out.exists():
        raise FileNotFoundError("No graph snapshots found")

    files = sorted(out.glob("*.gpickle"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError("No graph snapshot files found")

    latest = files[0]

    # Try to load via networkx gpickle reader (import lazily)
    try:
        import networkx.readwrite.gpickle as gpickle
        G = gpickle.read_gpickle(latest)
        return G
    except Exception:
        pass

    try:
        import networkx as nx
        if hasattr(nx, "read_gpickle"):
            return nx.read_gpickle(latest)
    except Exception:
        pass

    # Fallback: use pickle
    import pickle
    with open(latest, "rb") as f:
        G = pickle.load(f)
    return G
