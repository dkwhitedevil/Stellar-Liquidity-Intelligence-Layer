import json
import os
from datetime import datetime
from typing import List

from scoring.score_all import get_all_scores


OUT_DIR = os.getcwd() + "/scores"
os.makedirs(OUT_DIR, exist_ok=True)


def serialize_score(s):
    return {
        "timestamp": s.timestamp.isoformat(),
        "entity": s.entity,
        "score_type": s.score_type,
        "value": float(s.value),
        "explanation": s.explanation,
    }


def compute_and_save_scores() -> List[dict]:
    scores = get_all_scores()
    data = [serialize_score(s) for s in scores]

    ts = datetime.utcnow().isoformat()
    out_path = f"{OUT_DIR}/scores_{ts}.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    return data


def load_latest_scores() -> List[dict]:
    files = [f"{OUT_DIR}/{f}" for f in os.listdir(OUT_DIR) if f.startswith("scores_") and f.endswith('.json')]
    files = sorted(files, key=lambda p: os.stat(p).st_mtime, reverse=True)
    if not files:
        return []
    latest_file = files[0]
    with open(latest_file) as f:
        return json.load(f)
