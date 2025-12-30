import numpy as np
from scoring.score_schema import Score
from scoring.normalization import min_max


def compute_stability(entity, signals):
    volatility = [float(s.value) for s in signals if s.metric in ("price_std",)]

    if not volatility:
        return None

    normalized = min_max(volatility)
    score = 1.0 - sum(normalized) / len(normalized)
    score = max(0.0, min(1.0, float(score)))

    return Score(
        timestamp=max(s.timestamp for s in signals),
        entity=entity,
        score_type="stability",
        value=score,
        explanation="Lower observed price volatility implies higher stability."
    )
