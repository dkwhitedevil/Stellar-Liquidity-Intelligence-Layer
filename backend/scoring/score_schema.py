from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Score:
    timestamp: datetime
    entity: str
    score_type: str      # reliability | stability
    value: float         # normalized [0, 1]
    explanation: str     # human-readable, no decisions
