import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.processing.extractor import JobExtractor

def test_job_extractor_skills_and_salary():
    extractor = JobExtractor()
    
    sample_text = "We are looking for a Python and FastAPI developer with DuckDB experience. Docker knowledge is a plus. Salary: RM 4,000 - RM 6,000 per month."
    
    result = extractor.parse_job(sample_text)
    
    # Assert skills are correctly matched case-insensitively / capitalized
    assert "PYTHON" in result["skills"]
    assert "FASTAPI" in result["skills"]
    assert "DUCKDB" in result["skills"]
    assert "DOCKER" in result["skills"]
    
    # Assert salary range is correctly captured
    assert result["salary_range"] == "RM 4,000 - RM 6,000"

def test_job_extractor_empty_text():
    extractor = JobExtractor()
    result = extractor.parse_job("No technical skills or salary mentioned here.")
    
    assert result["skills"] == []
    assert result["salary_range"] == "Not Specified"