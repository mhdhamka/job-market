import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_jobs_endpoint():
    response = client.get("/jobs?limit=5")
    assert response.status_code == 200
    # Response should be a list of job records
    assert isinstance(response.json(), list)