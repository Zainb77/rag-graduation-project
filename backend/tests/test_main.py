from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "RAG Backend Service Running"}

def test_empty_query():
    response = client.post("/query", json={"question": ""})
    assert response.status_code == 400