import numpy as np
from scoring.score_schema import Score
from scoring.normalization import min_max


def compute_reliability(entity, signals):
    # Reliability = consistency (low std) of activity & liquidity signals
    activity = [float(s.value) for s in signals if s.metric in ("trade_count", "trade_volume")]
    liquidity = [float(s.value) for s in signals if s.metric in ("bid_depth", "ask_depth")]

    raw = []
    if activity:
        raw.append(float(np.std(activity, ddof=0)))
    if liquidity:
        raw.append(float(np.std(liquidity, ddof=0)))

    if not raw:
        return None

    normalized = min_max(raw)
    score = 1.0 - sum(normalized) / len(normalized)
    score = max(0.0, min(1.0, float(score)))

    return Score(
        timestamp=max(s.timestamp for s in signals),
        entity=entity,
        score_type="reliability",
        value=score,
        explanation="Lower variability in activity and liquidity implies higher reliability."
    )
