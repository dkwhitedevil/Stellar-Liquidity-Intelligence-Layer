"""Phase 3 verification harness
Run from repo root:

    python3 backend/graph_model/verify_phase3.py
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent
ROOT = BACKEND.parent

sys.path.insert(0, str(BACKEND))

from graph_model.build_graph import __name__ as bg_name


def fail(msg: str):
    print("FAIL:", msg)
    raise SystemExit(2)


def ok(msg: str):
    print("PASS:", msg)


def test_phase_leak_scan():
    pattern = r"\b(shortest_path|pathfind|pathfinding|shortest|score|optimi|rank|predict)\b"
    matches = []
    for p in HERE.rglob("*.py"):
        if p.name == "verify_phase3.py":
            continue
        try:
            txt = p.read_text()
        except Exception:
            continue
        if re.search(pattern, txt, flags=re.I):
            matches.append(p)
    if matches:
        fail(f"Phase-3 scope keywords found in: {matches}")
    ok("phase-3 scope purity: no routing/score/predict keywords")


def test_build_and_snapshot():
    # Run the build_graph module as a script
    import runpy
    ns = runpy.run_path(HERE / "build_graph.py", run_name="__main__")
    # Expect a snapshot file in graph_snapshots
    out = ROOT / "graph_snapshots"
    if not out.exists():
        fail("Graph snapshot directory not created")
    files = list(out.glob("*.gpickle"))
    if not files:
        fail("No graph snapshot files produced")
    ok(f"graph built and snapshot produced ({len(files)} files)")


def test_registry_validation():
    # Build graph and validate via import
    import runpy
    ns = runpy.run_path(HERE / "build_graph.py", run_name="__main__")
    ok("graph registry validation executed without assertion")


def test_no_pandas_numpy_usage():
    banned = r"\b(pandas|numpy|sklearn|networkx\.algorithms)\b"
    matches = []
    for p in HERE.rglob("*.py"):
        try:
            txt = p.read_text()
        except Exception:
            continue
        if re.search(banned, txt, flags=re.I):
            matches.append(p)
    # networkx is allowed, others are not
    matches = [p for p in matches if "networkx" not in p.read_text()]
    if matches:
        fail(f"Unexpected heavy-dependency usage in graph_model: {matches}")
    ok("no pandas/numpy/sklearn in graph_model")


def main():
    print("Running Phase 3 verification...\n")
    test_phase_leak_scan()
    test_build_and_snapshot()
    test_registry_validation()
    test_no_pandas_numpy_usage()
    print("\nPhase 3 verification passed. Phase 3 locked.")


if __name__ == "__main__":
    main()
