from analysis.simulate_phase7 import run_simulation


def test_simulation_improves():
    out_dir, summary = run_simulation(num_assets=8, n_per_path=20, seed=123)
    # Expect SLIL average success >= baseline
    assert summary['slil_avg_success'] >= summary['baseline_avg_success'] - 1e-6
    # Expect the summary keys exist
    assert 'baseline_avg_success' in summary and 'slil_avg_success' in summary
