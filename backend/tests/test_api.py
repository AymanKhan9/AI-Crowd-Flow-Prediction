import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "crowd-flow-api"}

def test_get_zones():
    response = client.get("/zones")
    assert response.status_code == 200
    assert "Gate_A" in response.json()["zones"]

def test_get_best_route_normal():
    # Test normal route without closure
    payload = {
        "start": "Gate_A",
        "end": "Exit",
        "accessibility": False,
        "emergency": False,
        "closed_zones": []
    }
    response = client.post("/best-route", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "path" in data
    assert data["path"][0] == "Gate_A"
    assert data["path"][-1] == "Exit"

def test_get_best_route_with_closures():
    # Test route with Gate_B closed
    payload = {
        "start": "Gate_B",
        "end": "Exit",
        "accessibility": False,
        "emergency": False,
        "closed_zones": ["Gate_B"]
    }
    # It should fail because start is closed
    response = client.post("/best-route", json=payload)
    assert response.status_code == 404
