import os
os.environ["DEMO_MODE"] = "true"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from app import app
from backend.database import init_db

init_db()
client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_register_login_and_planner():
    email = "test-pocket@example.com"
    client.post("/api/register", json={"name":"Tester","email":email,"password":"secret123"})
    r = client.post("/api/login", json={"email":email,"password":"secret123"})
    assert r.status_code == 200
    r = client.get("/api/session-info")
    assert r.json()["logged_in"] is True
    r = client.post("/api/generate-home", json={"budget":20000,"rooms":["Living Room"],"style":"Modern","notes":""})
    assert r.status_code == 200
    assert r.json()["planner"] == "home"
