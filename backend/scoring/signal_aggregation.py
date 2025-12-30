from collections import defaultdict
from typing import Iterable


def group_signals_by_entity(signals: Iterable):
    grouped = defaultdict(list)
    for s in signals:
        grouped[s.entity].append(s)
    return grouped
