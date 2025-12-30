import numpy as np


def ema_forecast(values, alpha=0.5):
    if not values:
        return 0.0
    ema = float(values[0])
    for v in values[1:]:
        ema = float(alpha) * float(v) + (1.0 - float(alpha)) * ema
    return float(ema)


def drift_forecast(values):
    if not values:
        return 0.0
    if len(values) < 2:
        return float(values[-1])
    return float(values[-1]) + (float(values[-1]) - float(values[0])) / float(len(values))
