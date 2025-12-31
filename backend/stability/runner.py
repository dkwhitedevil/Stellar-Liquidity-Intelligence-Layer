import json
import os
from datetime import datetime
from typing import List

from stability.temporal_stability import compute_temporal_stability
from signal_processing.extract_all_signals import get_all_signals


OUT_DIR = os.path.join(os.getcwd(), "stability")
os.makedirs(OUT_DIR, exist_ok=True)


def serialize_record(r):
    return {
        "timestamp": r.timestamp.isoformat(),
        "entity": r.entity,
        "metric": r.metric,
        "stability_index": float(r.stability_index),
        "variability": float(r.variability),
        "trend": float(r.trend),
        "sample_count": int(r.sample_count),
        "explanation": r.explanation,
    }


def compute_and_save_stability(window_size: int = 6, window_minutes: int = 5) -> List[dict]:
    signals = get_all_signals()
    records = compute_temporal_stability(signals, window_size=window_size, window_minutes=window_minutes)

    data = [serialize_record(r) for r in records]
    ts = datetime.utcnow().isoformat()
    out_path = f"{OUT_DIR}/stability_{ts}.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    return data


def load_latest_stability() -> List[dict]:
    files = [f"{OUT_DIR}/{f}" for f in os.listdir(OUT_DIR) if f.startswith("stability_") and f.endswith('.json')]
    files = sorted(files, key=lambda p: os.stat(p).st_mtime, reverse=True)
    if not files:
        return []
    latest = files[0]
    with open(latest) as f:
        return json.load(f)
