from datetime import datetime, timedelta
from stability.temporal_stability import compute_temporal_stability
from signal_processing.signal_schema import Signal


def test_compute_basic():
    now = datetime.utcnow().replace(second=0, microsecond=0)
    snaps = []
    # Create signals across 4 windows for entity E1, metric 'price_std'
    for i in range(4):
        ts = now - timedelta(minutes=5 * (3 - i))
        # Signal(timestamp, entity, dimension, metric, value, unit, source)
        snaps.append(Signal(ts, 'E1', 'volatility', 'price_std', 0.1 * (i + 1), 'price', 'trades'))

    records = compute_temporal_stability(snaps, window_size=4, window_minutes=5)
    assert isinstance(records, list)
    rec = next((r for r in records if r.entity == 'E1' and r.metric == 'price_std'), None)
    assert rec is not None
    assert rec.sample_count == 4
    assert 0.0 <= rec.stability_index <= 1.0
