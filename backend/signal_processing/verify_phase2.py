"""Phase 2 verification harness

Run this from the repo root (recommended):

    python backend/signal_processing/verify_phase2.py

Exit codes:
  0 - all tests passed
  >0 - failure
"""
from __future__ import annotations

import sys
import re
from pathlib import Path
from typing import List
from datetime import datetime

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent
ROOT = BACKEND.parent

# Ensure we import the backend package-local signal_processing
sys.path.insert(0, str(BACKEND))

from signal_processing.extract_all_signals import get_all_signals
from signal_processing.snapshot_loader import load


def fail(msg: str, code: int = 2):
    print("FAIL:", msg)
    raise SystemExit(code)


def ok(msg: str):
    print("PASS:", msg)


def test_0_precondition():
    # Test 0 — Precondition: snapshot dirs exist
    required = ["trades", "payments", "ledgers", "orderbooks"]
    base = BACKEND / "data" / "raw" / "snapshots"
    missing = [d for d in required if not (base / d).exists()]
    if missing:
        fail(f"Missing snapshot subdirectories: {missing}")
    ok("precondition: snapshot folders present")


def search_files(pattern: str) -> List[Path]:
    paths = []
    for p in sorted(HERE.rglob("*.py")):
        # Avoid self-matching (the pattern may appear in this verifier)
        if p == Path(__file__):
            continue
        try:
            text = p.read_text()
        except Exception:
            continue
        if re.search(pattern, text, flags=re.I):
            paths.append(p)
    return paths


def test_2_no_network_calls():
    # Test 2 — No network/horizon tokens in signal_processing
    banned = r"stellar_sdk|\bServer\b|horizon"
    matches = search_files(banned)
    if matches:
        fail(f"Network/horizon references found in: {matches}")
    ok("no horizon or stellar network references in signal_processing")


def test_6_scope_violation_scan():
    # Avoid false positives on common identifiers like 'Path' or 'path' variables.
    # We only flag substantive keywords such as 'graph' and pathfinding terms like 'pathfind' or 'shortest_path'.
    banned = r"\b(graph|pathfind|pathfinding|shortest_path|score|optimi|predict|model)\b"
    matches = search_files(banned)
    if matches:
        fail(f"Phase-2 scope keywords found in: {matches}")
    ok("scope purity: no phase-3/4 keywords present")


def serialize_signal(s):
    # Convert Signal into comparable tuple
    ts = getattr(s, "timestamp")
    # pandas.Timestamp or datetime
    try:
        iso = ts.isoformat()
    except Exception:
        iso = str(ts)
    return (iso, s.entity, s.dimension, s.metric, float(s.value), s.unit, s.source)


def test_full_pipeline_and_determinism():
    # Test 1 & 3 & 5 — run pipeline and determinism
    sigs_a = get_all_signals()
    sigs_b = get_all_signals()

    if not isinstance(sigs_a, list):
        fail("get_all_signals() did not return a list")

    ok("pipeline executed (returned list)")

    if len(sigs_a) != len(sigs_b):
        fail("Determinism failure: different number of signals between runs")

    sa = [serialize_signal(s) for s in sigs_a]
    sb = [serialize_signal(s) for s in sigs_b]

    if sa != sb:
        # Write a small diff for debugging
        for i, (x, y) in enumerate(zip(sa, sb)):
            if x != y:
                fail(f"Determinism failure at index {i}: {x} != {y}")

    ok(f"determinism: consistent across runs ({len(sa)} signals)")
    return sigs_a


def test_signal_object_integrity(signals):
    # Test 4 — object integrity and sample print
    print("Sample signals (up to 5):")
    for s in signals[:5]:
        print(s)

    for s in signals:
        # timestamp exists
        ts = getattr(s, "timestamp", None)
        if ts is None:
            fail(f"Signal missing timestamp: {s}")
        # value numeric
        try:
            v = float(s.value)
        except Exception:
            fail(f"Signal value not numeric float: {s}")
        # unit not None
        if s.unit is None:
            fail(f"Signal unit is None: {s}")
    ok("signal object integrity: timestamps, numeric values, units OK")


def test_time_alignment(signals):
    # Test 8 — time alignment: pick signals with same entity & metric
    import pandas as pd

    # select trade-type signals (they should be windowed)
    trade_signals = [s for s in signals if s.source == "trades"]
    if not trade_signals:
        ok("no trade signals present to test time alignment (OK)")
        return

    # group by (entity, metric)
    from collections import defaultdict

    groups = defaultdict(list)
    for s in trade_signals:
        groups[(s.entity, s.metric)].append(s)

    # For each group, check timestamps are floor-aligned to 5min
    for key, grp in groups.items():
        if len(grp) < 2:
            continue
        times = pd.to_datetime([getattr(s, "timestamp") for s in grp])
        floors = times.floor("5min")
        if not (floors == times).all():
            fail(f"Time alignment failure for group {key}")

    ok("time alignment: trade signals are 5-min window aligned")


def main():
    print("Running Phase 2 verification protocol...\n")
    test_0_precondition()
    test_2_no_network_calls()
    test_6_scope_violation_scan()
    signals = test_full_pipeline_and_determinism()
    test_signal_object_integrity(signals)
    test_time_alignment(signals)

    # Final human-check reminder
    print("\nHuman check: verify economic meaning of signals (trade_count, bid_depth, price_std, payment_count)\n")

    # If we made it here, all automatic checks passed
    print("Phase 2 fully tested and locked.")


if __name__ == "__main__":
    main()
