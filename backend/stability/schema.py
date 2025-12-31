from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class StabilityRecord:
    timestamp: datetime
    entity: str
    metric: str
    stability_index: float    # normalized measure in (0,1], higher => more stable
    variability: float        # observed std of recent windows
    trend: float              # slope estimate over recent windows
    sample_count: int
    explanation: Optional[str] = None
