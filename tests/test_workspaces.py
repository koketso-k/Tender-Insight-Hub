from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_workspace():
    response = client.post("/workspaces/", json={"name": "Test Workspace", "description": "Demo"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Workspace"
