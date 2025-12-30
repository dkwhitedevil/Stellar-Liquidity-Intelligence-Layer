from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class RouteAdvisory:
    timestamp: datetime
    source: str
    destination: str
    path: List[str]
    score: float              # advisory score (dimensionless)
    risk: float               # aggregated uncertainty
    explanation: str
