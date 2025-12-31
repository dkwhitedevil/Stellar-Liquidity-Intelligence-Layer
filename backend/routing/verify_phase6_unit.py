"""Simple Phase 6 smoke tests runner (no pytest required).
Run:
    python3 backend/routing/verify_phase6_unit.py
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent
sys.path.insert(0, str(BACKEND))

from routing.recommendation import run_recommendation


def _make_graph():
    # Minimal graph structure compatible with networkx-like interface
    class G(dict):
        def has_edge(self, u, v):
            return (u, v) in self
        def get_edge_data(self, u, v):
            return self.get((u, v), {})
    G = G()
    G[("A", "B")] = {"liquidity": 100}
    G[("B", "C")] = {"liquidity": 80}
    G[("A", "C")] = {"liquidity": 10}
    return G


def fake_scores_forecasts():
    class S:
        def __init__(self, entity, score_type, value):
            self.entity = entity
            self.score_type = score_type
            self.value = value

    class F:
        def __init__(self, entity, metric, uncertainty=0.01):
            self.entity = entity
            self.metric = metric
            self.uncertainty = uncertainty

    scores = [S("A", "reliability", 0.9), S("A", "stability", 0.9),
              S("B", "reliability", 0.8), S("B", "stability", 0.8),
              S("C", "reliability", 0.4), S("C", "stability", 0.4)]
    forecasts = [F("A", "payment_count"), F("B", "payment_count"), F("C", "payment_count")]
    return scores, forecasts


def run_smoke():
    G = _make_graph()
    scores, forecasts = fake_scores_forecasts()

    import routing.recommendation as recmod

    # monkeypatch module-level functions
    recmod.load_latest_graph = lambda: G
    recmod.get_all_scores = lambda: scores
    recmod.get_all_forecasts = lambda: forecasts

    # provide simple path enumerator that works on dict-based graph
    def simple_enum(G_, source, destination, max_hops=3):
        adj = {}
        for (u,v) in [k for k in G_.keys()]:
            adj.setdefault(u, []).append(v)
        results = []
        def dfs(curr, dest, path):
            if len(path)-1 > max_hops:
                return
            if curr == dest:
                results.append(list(path))
                return
            for nb in adj.get(curr, []):
                if nb in path:
                    continue
                path.append(nb)
                dfs(nb, dest, path)
                path.pop()
        dfs(source, destination, [source])
        return results

    recmod.enumerate_paths = simple_enum

    # run without filters
    recs = run_recommendation("A", "C")
    assert isinstance(recs, list), "Expected list of recommendations"
    assert len(recs) >= 1, "Expected at least one recommendation"

    # run with banned B — should return direct A->C only
    recs2 = run_recommendation("A", "C", banned=["B"])
    assert len(recs2) == 1
    assert recs2[0]["advisory"].path == ["A", "C"]

    # run with min_liq 50 — should return A->B->C only
    recs3 = run_recommendation("A", "C", min_liquidity=50)
    assert len(recs3) == 1
    assert recs3[0]["advisory"].path == ["A", "B", "C"]

    print("Phase 6 unit smoke tests passed.")


if __name__ == "__main__":
    run_smoke()
