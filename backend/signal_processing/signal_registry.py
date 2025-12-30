from typing import List
from signal_processing.signal_schema import Signal


def validate(signals: List[Signal]):
    for s in signals:
        assert isinstance(s.value, float), f"Signal value must be float, got {type(s.value)} for {s}"
        assert s.unit is not None, f"Signal unit cannot be None for {s}"
