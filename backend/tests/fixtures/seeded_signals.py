from datetime import datetime, timedelta
from signal_processing.signal_schema import Signal


def generate_seeded_signals(n=50, base_prefix='A', counter_prefix='B'):
    now = datetime(2025, 1, 1, 0, 0, 0)  # deterministic fixed timestamp for fixtures
    signals = []
    for i in range(n):
        ts = now - timedelta(minutes=i)
        base = f"{base_prefix}{i%5}"
        counter = f"{counter_prefix}{(i+1)%5}"
        pair = f"{base}/{counter}"
        signals.append(Signal(ts, pair, "liquidity", "trade_volume", float(100 + i), "units", "trades"))
    signals.append(Signal(now, f"{base_prefix}0/USDC", "liquidity", "trade_volume", 999.0, "units", "trades"))
    return signals
