from fastapi.testclient import TestClient
from api.main import app


def test_stability_endpoints(monkeypatch):
    # monkeypatch compute to return deterministic data
    def fake_compute(window_size=6, window_minutes=5):
        return [{"timestamp":"2025-01-01T00:00:00","entity":"E1","metric":"price_std","stability_index":0.9,"variability":0.1,"trend":0.0,"sample_count":4}]

    monkeypatch.setattr('stability.runner.compute_and_save_stability', fake_compute)

    client = TestClient(app)
    r = client.get('/stability/compute')
    assert r.status_code == 200
    body = r.json()
    assert body.get('computed') is True
    assert body.get('count') == 1

    r2 = client.get('/stability/latest')
    assert r2.status_code == 200
    b2 = r2.json()
    assert 'stability' in b2
