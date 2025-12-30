"""Phase 5 verification harness
Run from repo root:

    python3 backend/forecasting/verify_phase5.py
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent
ROOT = BACKEND.parent

sys.path.insert(0, str(BACKEND))

from forecasting.forecast_all import get_all_forecasts
from forecasting.forecast_registry import validate_forecasts


def fail(msg: str):
    print("FAIL:", msg)
    raise SystemExit(2)


def ok(msg: str):
    print("PASS:", msg)


def test_scope_scan():
    pattern = r"\b(path|route|select|recommend|optimi|best)\b"
    matches = []
    for p in HERE.rglob("*.py"):
        if p.name == "verify_phase5.py":
            continue
        try:
            txt = p.read_text()
        except Exception:
            continue
        if re.search(pattern, txt, flags=re.I):
            matches.append(p)
    if matches:
        fail(f"Phase-5 scope keywords found in: {matches}")
    ok("scope purity: no routing/selection/optimization keywords")


def test_no_thresholds_pattern():
    pattern = r"if\s+.*>"
    matches = []
    for p in HERE.rglob("*.py"):
        try:
            txt = p.read_text()
        except Exception:
            continue
        if re.search(pattern, txt):
            matches.append(p)
    if matches:
        fail(f"Threshold-like constructs found in forecasting: {matches}")
    ok("no threshold-like 'if ... >' constructs in forecasting")


def test_forecast_generation_and_validation():
    f1 = get_all_forecasts()
    f2 = get_all_forecasts()

    if len(f1) != len(f2):
        fail("Determinism failure: different number of forecasts between runs")

    # Validate registry
    validate_forecasts(f1)
    ok(f"forecast generation and registry validation passed ({len(f1)} forecasts)")


def main():
    print("Running Phase 5 verification...\n")
    test_scope_scan()
    test_no_thresholds_pattern()
    test_forecast_generation_and_validation()

    print("\nPhase 5 verification passed. Phase 5 locked.")


if __name__ == "__main__":
    main()
