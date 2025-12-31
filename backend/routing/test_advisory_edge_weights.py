from datetime import datetime
import networkx as nx
from routing.advise_routes import run_advisory


def make_graph(agg_mean, agg_uncertainty, agg_count=50):
    G = nx.MultiDiGraph()
    G.add_node('A0')
    G.add_node('USDC')
    G.add_edge('A0', 'USDC', agg_uncertainty=agg_uncertainty, agg_count=agg_count, agg_mean=agg_mean, metric='trade_volume')
    return G


def fake_scores_forecasts():
    from scoring.score_schema import Score
    from forecasting.forecast_schema import Forecast
    from datetime import datetime

    ts = datetime.utcnow()

    scores = [
        Score(ts, 'A0', 'reliability', 0.9, ''),
        Score(ts, 'A0', 'stability', 0.9, ''),
        Score(ts, 'USDC', 'reliability', 0.9, ''),
        Score(ts, 'USDC', 'stability', 0.9, ''),
    ]

    forecasts = [
        Forecast(ts, 'A0', 'payment_count', 'next_window', 10.0, 9.0, 11.0, 0.1, 'baseline'),
        Forecast(ts, 'USDC', 'payment_count', 'next_window', 10.0, 9.0, 11.0, 0.1, 'baseline')
    ]

    return scores, forecasts


def test_trade_volume_reduces_penalty(monkeypatch):
    import graph_model.graph_snapshot as gs
    import scoring.score_all as sa
    import forecasting.forecast_all as fa

    scores, forecasts = fake_scores_forecasts()
    monkeypatch.setattr(sa, 'get_all_scores', lambda: scores)
    monkeypatch.setattr(fa, 'get_all_forecasts', lambda: forecasts)

    # low-volume graph
    monkeypatch.setattr(gs, 'load_latest_graph', lambda: make_graph(agg_mean=1.0, agg_uncertainty=0.05, agg_count=50))
    adv_low = run_advisory('A0', 'USDC')
    s_low = adv_low[0].score if adv_low else 0.0

    # high-volume graph
    monkeypatch.setattr(gs, 'load_latest_graph', lambda: make_graph(agg_mean=20000.0, agg_uncertainty=0.05, agg_count=50))
    adv_high = run_advisory('A0', 'USDC')
    s_high = adv_high[0].score if adv_high else 0.0

    assert s_high >= s_low
