from datetime import datetime
from routing.route_schema import RouteAdvisory

from fastapi.testclient import TestClient


def test_graph_paths_endpoint(monkeypatch):
    # Fake advisory runner
    def fake_run_advisory(src, dst, max_hops=3):
        return [RouteAdvisory(datetime.utcnow(), src, dst, path=[src, dst], score=0.8, risk=0.05, explanation="ok")]

    monkeypatch.setattr('routing.advise_routes.run_advisory', fake_run_advisory)

    from api.main import app
    client = TestClient(app)

    # when src == dst -> empty
    r = client.get('/graph/paths?from=A&to=A')
    assert r.status_code == 200
    assert r.json() == []

    r = client.get('/graph/paths?from=X&to=Y')
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert data[0]["source"] == "X"
    assert data[0]["destination"] == "Y"
