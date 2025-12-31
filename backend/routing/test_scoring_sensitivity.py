def test_scoring_sensitivity_runs(monkeypatch, tmp_path):
    # Run a very small sweep and ensure it produces an output file
    import os
    from analysis.scoring_sensitivity import run_sweep

    monkeypatch.setenv('SLIL_SCARCITY_WEIGHT', '0.5')
    monkeypatch.setenv('SLIL_VOLUME_WEIGHT', '0.3')

    path = run_sweep([0.5], [0.3])
    assert path is not None
    assert os.path.exists(path)
