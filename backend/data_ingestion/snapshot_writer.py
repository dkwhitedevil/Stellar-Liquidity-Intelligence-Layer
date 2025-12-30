import json
from datetime import datetime
from pathlib import Path

BASE_PATH = Path("data/raw/snapshots")


def write_snapshot(kind: str, payload: dict):
    """
    Writes raw Horizon payloads with timestamped filenames
    for deterministic offline replay.
    """
    timestamp = datetime.utcnow().isoformat()
    path = BASE_PATH / kind
    path.mkdir(parents=True, exist_ok=True)

    filename = f"{timestamp}.json"
    full_path = path / filename

    with open(full_path, "w") as f:
        json.dump(payload, f, indent=2)

    return str(full_path)
