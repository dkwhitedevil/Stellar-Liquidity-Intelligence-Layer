from collections import defaultdict
from math import sqrt
from datetime import datetime

# Aggregates Phase-2 signals into per-edge summaries
# Keying: (source, target, metric)

def aggregate_signals(signals):
    """Return dict keyed by (src, dst, metric) -> summary dict with count, mean, std, last_ts, uncertainty."""
    buckets = defaultdict(lambda: {"values": [], "times": []})

    for s in signals:
        # For pair signals (BASE/COUNTER) aggregate under (BASE, COUNTER, metric)
        if "/" in s.entity:
            base, counter = s.entity.split("/", 1)
            # Treat pair directionally for aggregation (we will copy for both directions later)
            key = (base, counter, s.metric)
            buckets[key]["values"].append(float(s.value))
            buckets[key]["times"].append(s.timestamp)
        else:
            # Network-like entities -> self key
            key = (s.entity, s.entity, s.metric)
            buckets[key]["values"].append(float(s.value))
            buckets[key]["times"].append(s.timestamp)

    summaries = {}

    for k, v in buckets.items():
        vals = v["values"]
        times = v["times"]
        n = len(vals)
        mean = sum(vals) / n if n > 0 else 0.0
        # population std (ddof=0)
        if n > 0:
            var = sum((x - mean) ** 2 for x in vals) / n
            std = var ** 0.5
        else:
            std = 0.0
        last_ts = max(times) if times else None
        uncertainty = std / (sqrt(n) if n > 0 else 1)

        summaries[k] = {
            "agg_count": n,
            "agg_mean": mean,
            "agg_std": std,
            "agg_uncertainty": uncertainty,
            "last_ts": last_ts,
            "metric": k[2]
        }

    return summaries
