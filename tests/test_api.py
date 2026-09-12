import sys
import pathlib
import pytest
import duckdb
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

@pytest.fixture(autouse=True)
def setup_test_db():
    """Ensure a dummy DuckDB and necessary tables exist before any test runs."""
    db_path = pathlib.Path("data/job_market.duckdb")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create the database, the 'job_listings' table, and insert a dummy row
    if not db_path.exists():
        conn = duckdb.connect(str(db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS job_listings (
                id VARCHAR,
                title VARCHAR,
                company VARCHAR,
                location VARCHAR,
                description VARCHAR,
                salary_min DOUBLE,
                salary_max DOUBLE,
                created_at TIMESTAMP,
                source VARCHAR,
                url VARCHAR
            )
        """)
        # Insert a valid test record so queries don't return unexpected errors or empty formatting issues
        conn.execute("""
            INSERT INTO job_listings VALUES (
                'test-id-1', 
                'Software Engineer', 
                'Tech Corp', 
                'Remote', 
                'Python development', 
                50000.0, 
                80000.0, 
                CURRENT_TIMESTAMP, 
                'test', 
                'http://example.com'
            )
        """)
        conn.close()

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