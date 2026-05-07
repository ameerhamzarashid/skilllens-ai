from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "ok"
    assert "database_connection" in payload
    assert "models" in payload


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    payload = response.json()

    assert payload["app"] == "SkillLens AI"
    assert payload["status"] == "running"