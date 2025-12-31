"""Phase 5 verification harness
Run from repo root:

    python3 backend/stability/verify_phase5.py
"""
from __future__ import annotations

import sys
import re
from pathlib import Path
import runpy

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent
ROOT = BACKEND.parent

sys.path.insert(0, str(BACKEND))

from stability.runner import compute_and_save_stability, load_latest_stability


def fail(msg: str):
    print("FAIL:", msg)
    raise SystemExit(2)


def ok(msg: str):
    print("PASS:", msg)


def test_compute_and_load():
    a = compute_and_save_stability(window_size=4, window_minutes=5)
    b = compute_and_save_stability(window_size=4, window_minutes=5)
    if len(a) != len(b):
        fail("Determinism failure: different number of stability records between runs")

    la = load_latest_stability()
    if not isinstance(la, list):
        fail("Latest stability payload invalid")

    ok("stability compute and load passed")


if __name__ == "__main__":
    print("Running Phase 5 verification...\n")
    test_compute_and_load()
    print("\nPhase 5 verification passed. Phase 5 locked.")
