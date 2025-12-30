import numpy as np


def safe_normalize(series):
    if series.std(ddof=0) == 0:
        return series * 0
    return (series - series.mean()) / series.std(ddof=0)
