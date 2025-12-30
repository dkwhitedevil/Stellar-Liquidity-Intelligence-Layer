def advisory_score(reliability, stability, risk):
    base = 0.5 * float(reliability) + 0.5 * float(stability)
    return max(0.0, min(1.0, float(base - risk)))
