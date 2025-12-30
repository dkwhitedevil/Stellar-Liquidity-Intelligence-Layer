from scoring.signal_aggregation import group_signals_by_entity
from scoring.reliability_model import compute_reliability
from scoring.stability_model import compute_stability
from scoring.score_registry import validate_scores
from signal_processing.extract_all_signals import get_all_signals


def get_all_scores():
    scores = []

    signals = get_all_signals()
    grouped = group_signals_by_entity(signals)

    for entity, sigs in grouped.items():
        r = compute_reliability(entity, sigs)
        s = compute_stability(entity, sigs)
        if r:
            scores.append(r)
        if s:
            scores.append(s)

    validate_scores(scores)
    return scores


if __name__ == "__main__":
    scores = get_all_scores()
    # Temporary hard assertion to enforce boundedness (judge-grade check)
    for s in scores:
        assert 0.0 <= s.value <= 1.0, f"Score out of bounds: {s}"

    print(f"Phase 4 complete. Generated {len(scores)} scores.")
    for s in scores:
        print(s)
