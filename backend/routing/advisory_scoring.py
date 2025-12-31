import os


# Configurable weighting constants (can be overridden via environment variables or passed explicitly)
SCARCITY_WEIGHT = float(os.getenv("SLIL_SCARCITY_WEIGHT", "0.5"))
VOLUME_WEIGHT = float(os.getenv("SLIL_VOLUME_WEIGHT", "0.3"))
DEFAULT_EDGE_PENALTY_SCALE = float(os.getenv("SLIL_EDGE_PENALTY_SCALE", "0.5"))


def advisory_score(reliability, stability, risk, edge_penalty=0.0, edge_penalty_scale=DEFAULT_EDGE_PENALTY_SCALE):
    """Compute the advisory score.

    - Base score is the mean of reliability and stability.
    - `risk` is subtracted (forecasted uncertainty / other risk factors).
    - `edge_penalty` is an extra penalty derived from per-edge aggregated uncertainty and low sampling counts.
    - `edge_penalty_scale` controls the influence of edge penalties on final score.
    """
    base = 0.5 * float(reliability) + 0.5 * float(stability)
    score = float(base - risk - float(edge_penalty_scale) * float(edge_penalty))
    return max(0.0, min(1.0, score))


def compute_path_edge_penalty(G, path, scarcity_weight=None, vol_weight=None):
    """Given a networkx MultiDiGraph and a path (list of nodes), compute an aggregate penalty.

    Penalty derived from per-edge aggregated attributes:
    - `agg_uncertainty` (higher -> worse)
    - `agg_count` (scarcity -> worse)
    - `agg_mean` for certain metrics like `trade_volume` (higher volume -> better)

    `scarcity_weight` and `vol_weight` can be passed to override defaults (useful for sensitivity testing).

    Returns a float where typical values are small (e.g., 0-1). Lower is better.
    """
    if scarcity_weight is None:
        scarcity_weight = SCARCITY_WEIGHT
    if vol_weight is None:
        vol_weight = VOLUME_WEIGHT

    if not G or not path or len(path) < 2:
        return 0.0

    penalties = []

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        data = G.get_edge_data(u, v)
        if not data:
            # missing edge — treat as high penalty
            penalties.append(1.0)
            continue

        agg_uncertainties = []
        agg_counts = []
        volume_factors = []

        for key, attrs in data.items():
            if attrs is None:
                continue
            try:
                uq = attrs.get("agg_uncertainty")
                cnt = attrs.get("agg_count")
                mean = attrs.get("agg_mean")
                metric = attrs.get("metric")

                if uq is not None:
                    agg_uncertainties.append(float(uq))
                if cnt is not None:
                    agg_counts.append(float(cnt))

                # If this edge represents trade_volume, compute a volume factor that reduces penalty
                if metric == "trade_volume" and mean is not None:
                    # volume factor in (0,1], larger mean -> smaller factor
                    mf = 1.0 / (1.0 + float(mean) / 1000.0)
                    volume_factors.append(mf)
            except Exception:
                continue

        if not agg_uncertainties:
            penalties.append(0.25)
            continue

        mean_uq = sum(agg_uncertainties) / len(agg_uncertainties)
        mean_cnt = (sum(agg_counts) / len(agg_counts)) if agg_counts else 0.0
        scarcity = 1.0 / (1.0 + mean_cnt)

        # combine components: uncertainty + scaled scarcity + scaled volume factor (if any)
        vol_component = (sum(volume_factors) / len(volume_factors)) if volume_factors else 0.5

        edge_pen = mean_uq + scarcity_weight * scarcity + vol_weight * vol_component
        penalties.append(edge_pen)

    if not penalties:
        return 0.0

    return sum(penalties) / len(penalties)
