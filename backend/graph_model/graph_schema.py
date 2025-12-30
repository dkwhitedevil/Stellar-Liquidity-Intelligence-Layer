from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str        # asset | network
    metadata: Dict


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    timestamp: datetime
    attributes: Dict      # raw economic signals only
