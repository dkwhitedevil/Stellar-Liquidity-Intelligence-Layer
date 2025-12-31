from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import math

import numpy as np
from stability.schema import StabilityRecord


def floor_to_window(ts: datetime, window_minutes: int = 5) -> datetime:
    # Align timestamp to the lower 5-minute window
    minute = (ts.minute // window_minutes) * window_minutes
    return datetime(ts.year, ts.month, ts.day, ts.hour, minute, 0)


def compute_temporal_stability(signals: List, window_size: int = 6, window_minutes: int = 5) -> List[StabilityRecord]:
    """Compute temporal stability per entity/metric using recent windows.

    - Groups signals into time windows (floor to `window_minutes`).
    - For each entity and metric, creates time-ordered series and computes:
      * variability = std of recent values
      * trend = slope of linear fit over recent values
      * stability_index = 1.0 / (1.0 + variability + abs(trend))  (in (0,1])

    Returns list of `StabilityRecord` objects.
    """
    # Group values by (entity, metric, window)
    buckets: Dict[Tuple[str, str, datetime], List[float]] = defaultdict(list)

    for s in signals:
        if not hasattr(s, "timestamp") or not hasattr(s, "entity"):
            continue
        w = floor_to_window(s.timestamp, window_minutes=window_minutes)
        buckets[(s.entity, s.metric, w)].append(float(s.value))

    # Build per-entity,metric time series
    series: Dict[Tuple[str, str], Dict[datetime, List[float]]] = defaultdict(dict)
    for (entity, metric, window), vals in buckets.items():
        series[(entity, metric)][window] = vals

    records: List[StabilityRecord] = []

    for (entity, metric), ws in series.items():
        # time-ordered windows
        ordered = sorted(ws.items(), key=lambda x: x[0])
        times = [t for t, _ in ordered]
        values = [sum(vs) / len(vs) for _, vs in ordered]  # aggregate per-window via mean

        if not values:
            continue

        # consider only the last `window_size` windows
        times_recent = times[-window_size:]
        vals_recent = values[-window_size:]

        n = len(vals_recent)
        variability = float(np.std(vals_recent, ddof=0)) if n > 0 else 0.0

        # compute trend: linear fit of index -> value
        if n >= 2:
            x = np.arange(n)
            y = np.array(vals_recent)
            # use polyfit degree 1
            slope, intercept = np.polyfit(x, y, 1)
            trend = float(slope)
        else:
            trend = 0.0

        # stability index heuristic: higher variability or trend magnitude reduces stability
        stability_index = 1.0 / (1.0 + variability + abs(trend))
        stability_index = max(0.0, min(1.0, float(stability_index)))

        ts = times_recent[-1] if times_recent else datetime.utcnow()

        records.append(
            StabilityRecord(
                timestamp=ts,
                entity=entity,
                metric=metric,
                stability_index=stability_index,
                variability=variability,
                trend=trend,
                sample_count=n,
                explanation="Stability computed from recent rolling windows"
            )
        )

    return records
