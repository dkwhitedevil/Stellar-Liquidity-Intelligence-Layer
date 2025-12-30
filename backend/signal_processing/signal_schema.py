from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Signal:
    timestamp: datetime
    entity: str          # asset-pair | network | corridor
    dimension: str       # liquidity | volatility | flow | activity
    metric: str          # specific measured quantity
    value: float
    unit: str
    source: str          # trades | orderbooks | payments | ledgers
