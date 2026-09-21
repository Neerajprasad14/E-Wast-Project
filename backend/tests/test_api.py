from fastapi.testclient import TestClient
from app.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_nearby_recycler_endpoint_returns_demo_record():
    with TestClient(app) as client:
        response = client.get("/api/recyclers/nearby", params={"latitude": 17.385, "longitude": 78.4867})
        assert response.status_code == 200
        assert response.json()[0]["id"] == "demo-hyd-01"
