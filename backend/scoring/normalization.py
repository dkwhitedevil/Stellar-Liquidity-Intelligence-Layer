import numpy as np


def min_max(series):
    if not series:
        return []
    mn = min(series)
    mx = max(series)
    if mx == mn:
        return [0.5 for _ in series]
    return [(x - mn) / (mx - mn) for x in series]
