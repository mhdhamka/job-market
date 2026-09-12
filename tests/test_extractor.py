import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.processing.extractor import JobExtractor

def test_job_extractor_expanded_skills_and_salary():
    extractor = JobExtractor()
    
    # Sample text incorporating skills across your expanded categories
    sample_text = (
        "We are looking for a Software Engineer proficient in Python, Go, and SQL. "
        "Experience with Airflow, DuckDB, and Pandas is required. "
        "Must know PostgreSQL, Redis, AWS, Docker, Kubernetes, Git, and FastAPI or React. "
        "Salary: RM 5,000 - RM 8,000 per month."
    )
    
    result = extractor.parse_job(sample_text)
    
    # Assert programming languages & data engineering skills match
    assert "PYTHON" in result["skills"]
    assert "GO" in result["skills"]
    assert "SQL" in result["skills"]
    assert "AIRFLOW" in result["skills"]
    assert "DUCKDB" in result["skills"]
    assert "PANDAS" in result["skills"]
    
    # Assert databases, cloud/devops & frameworks match
    assert "POSTGRESQL" in result["skills"]
    assert "REDIS" in result["skills"]
    assert "AWS" in result["skills"]
    assert "DOCKER" in result["skills"]
    assert "KUBERNETES" in result["skills"]
    assert "GIT" in result["skills"]
    assert "FASTAPI" in result["skills"]
    assert "REACT" in result["skills"]
    
    # Assert salary range is correctly captured
    assert result["salary_range"] == "RM 5,000 - RM 8,000"

def test_job_extractor_empty_text():
    extractor = JobExtractor()
    result = extractor.parse_job("No technical skills or salary mentioned here.")
    
    assert result["skills"] == []
    assert result["salary_range"] == "Not Specified"