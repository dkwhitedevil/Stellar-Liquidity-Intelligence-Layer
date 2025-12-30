def validate_scores(scores):
    for s in scores:
        assert 0.0 <= s.value <= 1.0, f"Score value out of bounds: {s}"
        assert s.score_type in ("reliability", "stability"), f"Invalid score_type: {s}"
