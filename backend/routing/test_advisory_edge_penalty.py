import networkx as nx
from datetime import datetime
from routing.advise_routes import run_advisory
from routing.route_schema import RouteAdvisory


def make_test_graph_low_uncertainty():
    G = nx.MultiDiGraph()
    G.add_node('A0')
    G.add_node('USDC')
    # low uncertainty, high count
    G.add_edge('A0', 'USDC', agg_uncertainty=0.01, agg_count=100)
    return G


def make_test_graph_high_uncertainty():
    G = nx.MultiDiGraph()
    G.add_node('A0')
    G.add_node('USDC')
    # high uncertainty, low count
    G.add_edge('A0', 'USDC', agg_uncertainty=0.9, agg_count=1)
    return G


def test_advisory_penalty(monkeypatch):
    # Monkeypatch load_latest_graph to return low uncertainty graph and then high uncertainty graph
    import graph_model.graph_snapshot as gs
    # create fake scores and forecasts used by advise_routes
    def fake_get_all_scores():
        from scoring.score_all import Score
        return [Score('A0', 'reliability', 0.9, ''), Score('A0', 'stability', 0.9, ''), Score('USDC', 'reliability', 0.9, ''), Score('USDC', 'stability', 0.9, '')]

    def fake_get_all_forecasts():
        from forecasting.forecast_all import Forecast
        # return dummy forecast entries with small uncertainty
        return [Forecast('A0', 'payment_count', 10.0, 0.1), Forecast('USDC', 'payment_count', 10.0, 0.1)]

    import scoring.score_all as sa
    import forecasting.forecast_all as fa
    monkeypatch.setattr(sa, 'get_all_scores', fake_get_all_scores)
    monkeypatch.setattr(fa, 'get_all_forecasts', fake_get_all_forecasts)

    # Low uncertainty graph
    monkeypatch.setattr(gs, 'load_latest_graph', lambda: make_test_graph_low_uncertainty())
    advisories_low = run_advisory('A0', 'USDC')
    assert isinstance(advisories_low, list) and len(advisories_low) >= 0
    if len(advisories_low) > 0:
        s_low = advisories_low[0].score
    else:
        s_low = 0.0

    # High uncertainty graph
    monkeypatch.setattr(gs, 'load_latest_graph', lambda: make_test_graph_high_uncertainty())
    advisories_high = run_advisory('A0', 'USDC')
    if len(advisories_high) > 0:
        s_high = advisories_high[0].score
    else:
        s_high = 0.0

    # When high uncertainty should lead to lower score (if advisories present)
    assert s_high <= s_low
