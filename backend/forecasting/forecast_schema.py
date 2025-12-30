from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Forecast:
    timestamp: datetime
    entity: str
    metric: str
    horizon: str          # e.g. "next_window"
    expected: float
    lower_bound: float
    upper_bound: float
    uncertainty: float
    model: str            # explicit model name
