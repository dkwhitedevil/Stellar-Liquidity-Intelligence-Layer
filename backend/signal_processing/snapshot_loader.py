import json
from pathlib import Path
from typing import Dict, List

ROOT = Path("data/raw/snapshots")

def load(kind: str) -> List[Dict]:
    path = ROOT / kind
    if not path.exists():
        return []

    snaps = []
    for p in sorted(path.glob("*.json")):
        data = json.loads(p.read_text())
        # Attach a deterministic snapshot time derived from the filename (if available)
        # Filename example: 2025-12-30T17:35:59.698445.json
        try:
            data["__snapshot_time"] = p.stem
        except Exception:
            pass
        snaps.append(data)

    return snaps
