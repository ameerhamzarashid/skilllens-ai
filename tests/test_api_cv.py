from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_cv_extract_skills_endpoint():
    response = client.post(
        "/cv/extract-skills",
        json={
            "text": "I have experience with Python, SQL, Power BI and Docker."
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert "python" in payload["skills"]
    assert "sql" in payload["skills"]
    assert "power bi" in payload["skills"]
    assert "docker" in payload["skills"]


def test_skills_extract_endpoint():
    response = client.post(
        "/skills/extract",
        json={
            "text": "The role needs FastAPI, PostgreSQL, machine learning and Azure."
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert "fastapi" in payload["skills"]
    assert "postgresql" in payload["skills"]
    assert "machine learning" in payload["skills"]
    assert "azure" in payload["skills"]