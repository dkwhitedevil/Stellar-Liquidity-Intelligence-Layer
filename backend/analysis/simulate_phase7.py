"""Deterministic simulation runner for Phase 7. Provides a simple CLI to run the Monte Carlo experiment and write artifacts."""
from pathlib import Path
from datetime import datetime
import json
import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

SEED = 42
ARTIFACT_DIR = Path("analysis/artifacts/phase7")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def make_synthetic_graph(num_assets=8, seed=SEED):
    rng = np.random.default_rng(seed)
    G = nx.DiGraph()
    assets = [f"A{i}" for i in range(num_assets)]
    for a in assets:
        G.add_node(a)
    for i in range(num_assets):
        for j in range(num_assets):
            if i == j:
                continue
            if rng.random() < 0.35:
                depth = float(rng.uniform(20, 200))
                spread = float(rng.uniform(0.0005, 0.01))
                vol = float(rng.uniform(0.001, 0.05))
                failure_rate = float(rng.uniform(0.0, 0.2))
                G.add_edge(assets[i], assets[j], depth=depth, spread=spread, volatility=vol, failure_rate=failure_rate)
    return G


def edge_score(attrs):
    depth = attrs.get('depth', 0.0)
    spread = attrs.get('spread', 0.01)
    vol = attrs.get('volatility', 0.01)
    failure = attrs.get('failure_rate', 0.1)
    depth_norm = np.tanh(depth / 100.0)
    spread_norm = min(spread / 0.01, 1.0)
    vol_norm = min(vol / 0.05, 1.0)
    fail_norm = min(failure / 0.2, 1.0)
    return 0.4 * depth_norm - 0.2 * spread_norm - 0.2 * vol_norm - 0.2 * fail_norm


def baseline_route(G, source, dest, mode='spread'):
    try:
        if mode == 'hop':
            return nx.shortest_path(G, source, dest)
        elif mode == 'spread':
            return nx.shortest_path(G, source, dest, weight=lambda u, v, d: d.get('spread', 1.0))
    except Exception:
        return None


def slil_route(G, source, dest, max_hops=4):
    try:
        paths = list(nx.all_simple_paths(G, source, dest, cutoff=max_hops))
    except Exception:
        return None
    best = None
    best_score = -1e9
    for p in paths:
        scores = []
        ok = True
        for u, v in zip(p[:-1], p[1:]):
            if not G.has_edge(u, v):
                ok = False
                break
            scores.append(edge_score(G.get_edge_data(u, v)))
        if not ok or not scores:
            continue
        s = sum(scores) / len(scores)
        if s > best_score:
            best_score = s
            best = p
    return best


def simulate_transactions(G, path, n=50, rng=None):
    if not path or len(path) < 2:
        return {'successes':0, 'attempts':0, 'avg_slippage':None}
    if rng is None:
        rng = np.random.default_rng(SEED)
    successes = 0
    slippages = []
    attempts = n
    for _ in range(n):
        failed = False
        total_slip = 0.0
        for u, v in zip(path[:-1], path[1:]):
            attrs = G.get_edge_data(u, v)
            fail_p = attrs.get('failure_rate', 0.1)
            if rng.random() < fail_p:
                failed = True
                break
            mean = attrs.get('spread', 0.001)
            sd = attrs.get('volatility', 0.01)
            slip = max(0.0, rng.normal(mean, sd))
            total_slip += slip
        if not failed:
            successes += 1
            slippages.append(total_slip)
    avg_slip = float(np.mean(slippages)) if slippages else None
    return {'successes':successes, 'attempts':attempts, 'success_rate': successes/attempts if attempts else 0.0, 'avg_slippage':avg_slip}


def run_simulation(num_assets=10, n_per_path=50, seed=SEED):
    rng = np.random.default_rng(seed+1)
    G = make_synthetic_graph(num_assets=num_assets, seed=seed)
    nodes = list(G.nodes())
    corridors = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            corridors.append((nodes[i], nodes[j]))
    results = []
    for (src, dst) in corridors:
        b_path = baseline_route(G, src, dst, mode='spread')
        s_path = slil_route(G, src, dst, max_hops=5)
        if not b_path and not s_path:
            continue
        b_res = simulate_transactions(G, b_path, n=n_per_path, rng=rng)
        s_res = simulate_transactions(G, s_path, n=n_per_path, rng=rng)
        results.append({
            'src':src, 'dst':dst,
            'baseline_success': b_res.get('success_rate', 0.0), 'baseline_slip': b_res.get('avg_slippage'),
            'slil_success': s_res.get('success_rate', 0.0), 'slil_slip': s_res.get('avg_slippage'),
            'b_path': b_path, 's_path': s_path
        })
    df = pd.DataFrame(results)
    summary = {
        'baseline_avg_success': float(df['baseline_success'].mean()),
        'slil_avg_success': float(df['slil_success'].mean()),
        'baseline_avg_slip': float(df['baseline_slip'].dropna().mean()) if not df['baseline_slip'].dropna().empty else None,
        'slil_avg_slip': float(df['slil_slip'].dropna().mean()) if not df['slil_slip'].dropna().empty else None,
    }

    out_dir = ARTIFACT_DIR / datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    out_dir.mkdir(parents=True, exist_ok=True)
    df.assign(improvement = df['slil_success'] - df['baseline_success']).to_csv(out_dir / 'phase7_summary.csv', index=False)

    # simple plot
    plt.figure(figsize=(6,4))
    plt.hist(df['baseline_success'].dropna(), alpha=0.6, label='Baseline')
    plt.hist(df['slil_success'].dropna(), alpha=0.6, label='SLIL')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / 'success_rate_hist.png')
    plt.close()

    manifest = {
        'seed': seed,
        'num_assets': num_assets,
        'n_per_path': n_per_path,
        'summary': summary,
    }
    with open(out_dir / 'manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    return out_dir, summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-assets', type=int, default=10)
    parser.add_argument('--n-per-path', type=int, default=50)
    parser.add_argument('--seed', type=int, default=SEED)
    args = parser.parse_args()

    out_dir, summary = run_simulation(num_assets=args.num_assets, n_per_path=args.n_per_path, seed=args.seed)
    print('Simulation saved to', out_dir)
    print(summary)
