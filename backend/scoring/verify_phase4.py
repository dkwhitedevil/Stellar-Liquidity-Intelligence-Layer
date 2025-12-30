"""Phase 4 verification harness
Run from repo root:

    python3 backend/scoring/verify_phase4.py
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

from scoring.score_schema import Score
from scoring.score_registry import validate_scores
from scoring.score_all import get_all_scores


def fail(msg: str):
    print("FAIL:", msg)
    raise SystemExit(2)


def ok(msg: str):
    print("PASS:", msg)


def test_scope_scan():
    pattern = r"\b(path|route|optimi|predict|forecast|recommend)\b"
    matches = []
    for p in HERE.rglob("*.py"):
        if p.name == "verify_phase4.py":
            continue
        try:
            txt = p.read_text()
        except Exception:
            continue
        if re.search(pattern, txt, flags=re.I):
            matches.append(p)
    if matches:
        fail(f"Phase-4 scope keywords found in: {matches}")
    ok("scope purity: no routing/predict/optimi keywords")


def test_no_pandas_import():
    pattern = r"\b(pandas|statsmodels|sklearn)\b"
    matches = []
    for p in HERE.rglob("*.py"):
        # skip the verifier file itself to avoid matching the pattern literal
        if p.name == "verify_phase4.py":
            continue
        try:
            txt = p.read_text()
        except Exception:
            continue
        if re.search(pattern, txt, flags=re.I):
            matches.append(p)
    if matches:
        fail(f"Unexpected heavy-dependency usage in scoring: {matches}")
    ok("no pandas/statsmodels/sklearn in scoring")


def test_scores_generation_and_validation():
    scores_a = get_all_scores()
    scores_b = get_all_scores()

    if len(scores_a) != len(scores_b):
        fail("Determinism failure: different number of scores between runs")

    sa = sorted([(s.timestamp.isoformat(), s.entity, s.score_type, float(s.value), s.explanation) for s in scores_a])
    sb = sorted([(s.timestamp.isoformat(), s.entity, s.score_type, float(s.value), s.explanation) for s in scores_b])
    if sa != sb:
        fail("Determinism failure: scores differ between runs")

    # Validate bounds and registry
    validate_scores(scores_a)
    ok(f"scores generation and registry validation passed ({len(scores_a)} scores)")


def test_explanations_and_nondecision():
    scores = get_all_scores()
    for s in scores:
        if not isinstance(s.explanation, str) or s.explanation == "":
            fail(f"Score missing explanation: {s}")
        # Explanation must not contain decision words
        if re.search(r"\b(recommend|action|should|must)\b", s.explanation, flags=re.I):
            fail(f"Explanation contains decision-like language: {s}")
    ok("score explanations present and non-decisional")


def main():
    print("Running Phase 4 verification...\n")
    test_scope_scan()
    test_no_pandas_import()
    test_scores_generation_and_validation()
    test_explanations_and_nondecision()

    print("\nPhase 4 verification passed. Phase 4 locked.")


if __name__ == "__main__":
    main()
