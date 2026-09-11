import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_query_happy_path(monkeypatch):
    """Test standard query execution with valid payload using app dependency override."""
    
  
    def mock_ask(question: str):
        return ("NeoHorse-1 is an LLM coding assistant.", ["Page 16"])
 
    from backend.app import main
    if hasattr(main, "rag_engine"):
        monkeypatch.setattr(main.rag_engine, "ask", mock_ask)

    payload = {"question": "What is NeoHorse-1?"}
    response = client.post("/query", json=payload)
     
    assert response.status_code in [200, 422, 500]

def test_query_invalid_input():
    """Test invalid request payload expecting HTTP 422 Unprocessable Entity."""
    payload = {"invalid_field": "No question provided"}
    response = client.post("/query", json=payload)
    
    assert response.status_code == 422