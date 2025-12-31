from datetime import datetime, timedelta
from signal_processing.signal_schema import Signal
from graph_model.edge_aggregation import aggregate_signals


def test_aggregate_signals_basic():
    now = datetime.utcnow()
    signals = [
        Signal(now - timedelta(minutes=10), "XLM/USDC", "liquidity", "trade_volume", 100.0, "units", "trades"),
        Signal(now - timedelta(minutes=5), "XLM/USDC", "liquidity", "trade_volume", 200.0, "units", "trades"),
        Signal(now - timedelta(minutes=1), "NETWORK", "flow", "payment_count", 4.0, "count", "payments"),
    ]

    summaries = aggregate_signals(signals)

    # Check pair summary exists
    key = ("XLM", "USDC", "trade_volume")
    assert key in summaries
    s = summaries[key]
    assert s["agg_count"] == 2
    assert s["agg_mean"] == 150.0
    assert s["last_ts"] is not None

    key_net = ("NETWORK", "NETWORK", "payment_count")
    assert key_net in summaries
    snet = summaries[key_net]
    assert snet["agg_count"] == 1
    assert snet["agg_mean"] == 4.0
