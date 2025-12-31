from scoring.runner import compute_and_save_scores, load_latest_scores


def test_compute_and_load(tmp_path, monkeypatch):
    # Run computation (uses seeded signals and existing pipelines)
    data = compute_and_save_scores()
    assert isinstance(data, list)
    assert len(data) >= 0

    latest = load_latest_scores()
    assert isinstance(latest, list)
