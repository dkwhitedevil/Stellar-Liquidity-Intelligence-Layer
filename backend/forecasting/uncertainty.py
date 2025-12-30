import numpy as np


def estimate_uncertainty(values):
    if len(values) < 2:
        return 0.0
    return float(np.std(values, ddof=0))
