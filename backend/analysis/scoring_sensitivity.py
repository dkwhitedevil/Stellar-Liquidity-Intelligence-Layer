"""Run a sensitivity sweep over scoring hyperparameters and report results.

Writes CSV summary to ./artifacts/scoring_sensitivity_{ts}.csv
"""
import argparse
import csv
import os
from datetime import datetime

from graph_model.build_graph import build_temporal_graph
from graph_model.node_builder import build_nodes
from graph_model.edge_builder import build_edges
from graph_model.graph_snapshot import save_graph_snapshot
from routing.advise_routes import run_advisory
from tests.fixtures import seeded_signals


def run_sweep(scarcity_weights, vol_weights):
    signals = seeded_signals.generate_seeded_signals(60)
    nodes = build_nodes(signals)
    edges = build_edges(signals)
    G = build_temporal_graph(nodes, edges)

    rows = []

    for sw in scarcity_weights:
        for vw in vol_weights:
            # Monkeypatch via calling compute_path_edge_penalty with explicit weights is not trivial from run_advisory,
            # so we rely on setting env vars used in defaults for the time being.
            os.environ["SLIL_SCARCITY_WEIGHT"] = str(sw)
            os.environ["SLIL_VOLUME_WEIGHT"] = str(vw)

            # Evaluate a sample corridor
            advisories = run_advisory("A0", "USDC")
            avg_score = sum(a.score for a in advisories) / len(advisories) if advisories else 0.0
            rows.append({"scarcity_weight": sw, "vol_weight": vw, "avg_score": avg_score})

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_dir = os.path.join(os.getcwd(), "artifacts")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"scoring_sensitivity_{ts}.csv")

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["scarcity_weight", "vol_weight", "avg_score"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Wrote sensitivity report: {path}")
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scarcity", nargs="+", type=float, default=[0.2, 0.5, 0.8])
    parser.add_argument("--volume", nargs="+", type=float, default=[0.1, 0.3, 0.6])
    args = parser.parse_args()

    run_sweep(args.scarcity, args.volume)
