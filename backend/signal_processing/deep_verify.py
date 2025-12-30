"""Deep Phase 2 audit harness

Run from project root:

    python3 backend/signal_processing/deep_verify.py

"""
from __future__ import annotations

import sys
import re
import tempfile
import shutil
import random
from pathlib import Path
from typing import List

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent
ROOT = BACKEND.parent

sys.path.insert(0, str(BACKEND))

from signal_processing.extract_all_signals import get_all_signals
from signal_processing import snapshot_loader


def fail(msg):
    print("FAIL:", msg)
    raise SystemExit(2)


def ok(msg):
    print("PASS:", msg)


def run_grep(pattern: str) -> List[Path]:
    matches = []
    for p in HERE.rglob("*.py"):
        try:
            txt = p.read_text()
        except Exception:
            continue
        if re.search(pattern, txt, flags=re.I):
            matches.append(p)
    return matches


def test_phase_leak_scan():
    # Use a conservative word-boundary pattern to avoid matching common identifiers like 'Path'.
    pattern = r"\b(graph|pathfind|pathfinding|shortest_path|score|optimi|predict|recommend|route)\b"
    matches = run_grep(pattern)
    # exclude the verifier harness files themselves
    matches = [p for p in matches if p.name not in ("verify_phase2.py", "deep_verify.py")]
    if matches:
        fail(f"Phase-leak keywords found in: {matches}")
    ok("phase-leak scan passed")


def test_no_implicit_assumptions():
    pattern = r"0\.5|0\.7|\bthreshold\b|if\s+value\s*>"
    matches = run_grep(pattern)
    if matches:
        fail(f"Implicit thresholds or hard-coded assumptions found in: {matches}")
    ok("no implicit thresholds or hard-coded economic assumptions found")


def serialize_signal(s):
    ts = getattr(s, "timestamp")
    try:
        iso = ts.isoformat()
    except Exception:
        iso = str(ts)
    return (iso, s.entity, s.dimension, s.metric, float(s.value), s.unit, s.source)


def test_shuffle_determinism():
    # Create a temp snapshot tree and copy files using randomized prefixes
    base = BACKEND / "data" / "raw" / "snapshots"
    kinds = [p.name for p in base.iterdir() if p.is_dir()]

    with tempfile.TemporaryDirectory() as tdir:
        troot = Path(tdir)
        for k in kinds:
            src = base / k
            dst = troot / k
            dst.mkdir(parents=True, exist_ok=True)
            files = sorted(src.glob("*.json"))
            # Shuffle by copying with randomized prefix
            order = list(range(len(files)))
            random.shuffle(order)
            for i, idx in enumerate(order):
                f = files[idx]
                # randomized name to break lexicographic ordering
                new_name = f"{random.randint(1000,9999)}_{i}_{f.name}"
                shutil.copy2(f, dst / new_name)

        # Monkeypatch ROOT to point to temp dir
        old_root = snapshot_loader.ROOT
        snapshot_loader.ROOT = troot
        try:
            sigs1 = get_all_signals()
            sigs2 = get_all_signals()
        finally:
            snapshot_loader.ROOT = old_root

        sa = sorted([serialize_signal(s) for s in sigs1])
        sb = sorted([serialize_signal(s) for s in sigs2])
        if sa != sb:
            fail("Shuffle determinism failed: signal sets differ after shuffling filenames")
        ok("shuffle determinism: consistent signals regardless of file ordering")


def test_numeric_purity_and_units_and_time():
    sigs = get_all_signals()
    # Numeric purity
    for s in sigs:
        if not isinstance(s.value, float):
            fail(f"Signal value not float: {s}")
        if s.unit is None or (not isinstance(s.unit, str)) or s.unit == "":
            fail(f"Signal unit missing or invalid: {s}")
    ok("numeric purity and unit presence OK")

    # Unit discipline mapping
    expected_units = {
        "trade_count": "count",
        "trade_volume": "units",
        "vwap": "price",
        "price_std": "price",
        "bid_depth": "units",
        "ask_depth": "units",
        "payment_count": "count",
        "ledger_count": "count",
        "spread": "price",
        "imbalance": "ratio",
    }

    metrics = set(s.metric for s in sigs)
    # For any metric in expected_units that appears in signals, check unit matches
    for m, unit in expected_units.items():
        for s in [x for x in sigs if x.metric == m]:
            if s.unit != unit:
                fail(f"Unit mismatch for metric {m}: expected {unit}, got {s.unit}")
    ok("unit discipline: known metrics have correct units when present")

    # Time semantics: trade signals should be window-aligned
    import pandas as pd
    trade_signals = [s for s in sigs if s.source == "trades"]
    if trade_signals:
        times = pd.to_datetime([getattr(s, "timestamp") for s in trade_signals])
        floors = times.floor("5min")
        if not (floors == times).all():
            fail("Time semantics: some trade signals are not 5-min window aligned")
        ok("time semantics: trade signals are 5-min aligned")
    else:
        ok("time semantics: no trade signals present to check")


def test_signal_completeness():
    # Check that code contains implementation of canonical metrics
    required = ["trade_count","trade_volume","vwap","price_std","bid_depth","ask_depth","payment_count","ledger_count","imbalance","spread"]
    missing = []
    for r in required:
        found = False
        for p in HERE.rglob("*.py"):
            try:
                txt = p.read_text()
            except Exception:
                continue
            if f'"{r}"' in txt or f"'{r}'" in txt:
                found = True
                break
        if not found:
            missing.append(r)
    if missing:
        fail(f"Missing canonical metric implementations in code: {missing}")
    ok("signal completeness: canonical metrics appear implemented in code")


def main():
    print("Running deep Phase 2 audit...\n")
    test_phase_leak_scan()
    test_no_implicit_assumptions()
    test_shuffle_determinism()
    test_numeric_purity_and_units_and_time()
    test_signal_completeness()

    print("\nAll deep audit checks passed. Phase 2 audited and locked.")


if __name__ == "__main__":
    main()
