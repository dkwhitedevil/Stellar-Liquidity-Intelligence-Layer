import networkx as nx
from routing.recommendation import run_recommendation


def _make_graph():
    G = nx.DiGraph()
    G.add_edge("A", "B", liquidity=100)
    G.add_edge("B", "C", liquidity=80)
    G.add_edge("A", "C", liquidity=10)
    return G


def test_banned_asset(monkeypatch):
    # Small graph with A->B->C and A->C
    G = _make_graph()

    def fake_load():
        return G

    # Provide deterministic scores & forecasts for A,B,C
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

    scores = [S("A", "reliability", 0.9), S("A", "stability", 0.9), S("B", "reliability", 0.8), S("B", "stability", 0.8), S("C", "reliability", 0.4), S("C", "stability", 0.4)]
    forecasts = [F("A", "payment_count"), F("B", "payment_count"), F("C", "payment_count")]

    monkeypatch.setattr('routing.recommendation.load_latest_graph', fake_load)
    monkeypatch.setattr('routing.recommendation.get_all_scores', lambda: scores)
    monkeypatch.setattr('routing.recommendation.get_all_forecasts', lambda: forecasts)

    # Ban B so only A->C direct should remain
    recs = run_recommendation("A", "C", banned=["B"])
    assert len(recs) == 1
    assert recs[0]["advisory"].path == ["A", "C"]


def test_min_liquidity_filter(monkeypatch):
    G = _make_graph()

    def fake_load():
        return G

    class S:
        def __init__(self, entity, score_type, value):
            self.entity = entity
            self.score_type = score_type
            self.value = value

    class F:
        def __init__(self, entity, metric, uncertainty=0.1):
            self.entity = entity
            self.metric = metric
            self.uncertainty = uncertainty

    scores = [S("A", "reliability", 0.9), S("A", "stability", 0.9), S("B", "reliability", 0.8), S("B", "stability", 0.8), S("C", "reliability", 0.4), S("C", "stability", 0.4)]
    forecasts = [F("A", "payment_count"), F("B", "payment_count"), F("C", "payment_count")]

    monkeypatch.setattr('routing.recommendation.load_latest_graph', fake_load)
    monkeypatch.setattr('routing.recommendation.get_all_scores', lambda: scores)
    monkeypatch.setattr('routing.recommendation.get_all_forecasts', lambda: forecasts)

    # min_liquidity=50 should exclude A->C (liquidity 10) but allow A->B->C
    recs = run_recommendation("A", "C", min_liquidity=50)
    assert len(recs) == 1
    assert recs[0]["advisory"].path == ["A", "B", "C"]
