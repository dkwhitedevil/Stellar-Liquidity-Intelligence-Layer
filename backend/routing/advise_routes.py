from datetime import datetime
from graph_model.graph_snapshot import load_latest_graph
from scoring.score_all import get_all_scores
from forecasting.forecast_all import get_all_forecasts
from routing.path_enumerator import enumerate_paths
from routing.advisory_scoring import advisory_score
from routing.risk_adjustment import risk_penalty
from routing.route_schema import RouteAdvisory
from routing.route_registry import validate_advisories
from routing.policy_filters import apply_policies


def run_advisory(source, destination, max_hops=3):
    scores = get_all_scores()
    forecasts = get_all_forecasts()

    score_map = {(s.entity, s.score_type): s for s in scores}
    forecast_map = {(f.entity, f.metric): f for f in forecasts}

    G = load_latest_graph()

    paths = enumerate_paths(G, source, destination, max_hops=max_hops)
    paths = apply_policies(paths, max_hops=max_hops)

    advisories = []

    for path in paths:
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
            continue

        avg_r = sum(m["reliability"] for m in metrics) / len(metrics)
        avg_s = sum(m["stability"] for m in metrics) / len(metrics)
        risk = risk_penalty(metrics)

        # Compute per-edge penalty from graph aggregated attributes
        edge_penalty = 0.0
        try:
            from routing.advisory_scoring import compute_path_edge_penalty
            edge_penalty = compute_path_edge_penalty(G, path)
        except Exception:
            edge_penalty = 0.0

        advisories.append(
            RouteAdvisory(
                timestamp=datetime.utcnow(),
                source=source,
                destination=destination,
                path=path,
                score=advisory_score(avg_r, avg_s, risk, edge_penalty=edge_penalty),
                risk=risk,
                explanation=(f"Advisory score balances historical reliability, stability, and forecast uncertainty. "
                             f"Edge penalty={edge_penalty:.3f}"),
            )
        )

    validate_advisories(advisories)
    return advisories


if __name__ == "__main__":
    # Example placeholders — these should be replaced by real canonical entity ids for actual advisories
    SOURCE = "credit_alphanum4/native"
    DEST = "native/credit_alphanum12"

    advisories = run_advisory(SOURCE, DEST)

    print(f"Phase 6 complete. Generated {len(advisories)} route advisories.")
    for a in advisories:
        print(a)
