from datetime import datetime
from routing.route_schema import RouteAdvisory


def fake_recs():
    return [{
        "advisory": RouteAdvisory(datetime.utcnow(), "A", "C", path=["A","C"], score=0.9, risk=0.02, explanation="ok"),
        "metrics": [{"reliability":0.9, "stability":0.9, "uncertainty":0.01}],
        "edge_penalty": 0.05,
        "min_liquidity": 10
    }]


def test_routes_recommend_endpoint(monkeypatch):
    monkeypatch.setattr('routing.recommendation.run_recommendation', lambda *args, **kwargs: fake_recs())
    from api.main import routes_recommend

    out = routes_recommend("A", "C")
    assert isinstance(out, list)
    assert len(out) == 1
    assert out[0]["path"] == ["A", "C"]
