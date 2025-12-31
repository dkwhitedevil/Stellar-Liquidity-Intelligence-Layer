from datetime import datetime
from typing import List, Optional
from graph_model.graph_snapshot import load_latest_graph
from scoring.score_all import get_all_scores
from forecasting.forecast_all import get_all_forecasts
from routing.path_enumerator import enumerate_paths
from routing.advisory_scoring import advisory_score, compute_path_edge_penalty
from routing.risk_adjustment import risk_penalty
from routing.route_schema import RouteAdvisory
from routing.policy_filters import apply_policies


def _path_has_banned_asset(path: List[str], banned: List[str]) -> bool:
    banned_set = set(banned or [])
    return any(p in banned_set for p in path)


def _path_min_liquidity(G, path: List[str]) -> Optional[float]:
    # Inspect adjacent edges for a 'liquidity' or 'agg_mean' metric, return minimum across edges
    vals = []
    for u, v in zip(path[:-1], path[1:]):
        if G.has_edge(u, v):
            e = G.get_edge_data(u, v)
            # networkx may store multiple keys for multigraph, select first mapping
            if isinstance(e, dict):
                # If it's a multigraph, dict of keys -> attrs
                if any(isinstance(k, int) for k in e.keys()):
                    # iterate items
                    for _k, attrs in e.items():
                        if not isinstance(attrs, dict):
                            continue
                        val = attrs.get("liquidity") or attrs.get("agg_mean") or attrs.get("agg_count")
                        if val is not None:
                            vals.append(float(val))
                            break
                else:
                    val = e.get("liquidity") or e.get("agg_mean") or e.get("agg_count")
                    if val is not None:
                        vals.append(float(val))
    if not vals:
        return None
    return min(vals)


def run_recommendation(source: str, destination: str, max_hops: int = 3, banned: Optional[List[str]] = None, min_liquidity: Optional[float] = None):
    """Produce ranked route recommendations between source and destination.

    Parameters
    - banned: list of asset/entity ids to exclude from candidate paths
    - min_liquidity: minimum per-edge liquidity required (if computable from graph)
    """
    scores = get_all_scores()
    forecasts = get_all_forecasts()

    score_map = {(s.entity, s.score_type): s for s in scores}
    forecast_map = {(f.entity, f.metric): f for f in forecasts}

    G = load_latest_graph()

    paths = enumerate_paths(G, source, destination, max_hops=max_hops)
    paths = apply_policies(paths, max_hops=max_hops)

    recommendations = []

    for path in paths:
        # policy filtering: banned assets
        if banned and _path_has_banned_asset(path, banned):
            continue

        # liquidity filtering (if requested and computable)
        if min_liquidity is not None:
            pmin = _path_min_liquidity(G, path)
            if pmin is not None and pmin < float(min_liquidity):
                continue

        metrics = []
        for node in path:
            r = score_map.get((node, "reliability"))
            s = score_map.get((node, "stability"))
            f = forecast_map.get((node, "payment_count"))

            if r and s and f:
                metrics.append({
                    "reliability": r.value,
                    "stability": s.value,
                    "uncertainty": f.uncertainty,
                })

        if not metrics:
            # skip paths with incomplete metrics
            continue

        avg_r = sum(m["reliability"] for m in metrics) / len(metrics)
        avg_s = sum(m["stability"] for m in metrics) / len(metrics)
        risk = risk_penalty(metrics)

        edge_penalty = 0.0
        try:
            edge_penalty = compute_path_edge_penalty(G, path)
        except Exception:
            edge_penalty = 0.0

        score = advisory_score(avg_r, avg_s, risk, edge_penalty=edge_penalty)

        recommendations.append({
            "advisory": RouteAdvisory(
                timestamp=datetime.utcnow(),
                source=source,
                destination=destination,
                path=path,
                score=score,
                risk=risk,
                explanation=(f"Recommendation balances reliability, stability and forecast uncertainty. Edge penalty={edge_penalty:.3f}"),
            ),
            "metrics": metrics,
            "edge_penalty": edge_penalty,
            "min_liquidity": _path_min_liquidity(G, path),
        })

    # sort by score descending
    recommendations.sort(key=lambda r: r["advisory"].score, reverse=True)

    return recommendations
