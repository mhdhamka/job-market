import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.processing.matcher import JobMatcher

def test_job_matcher_perfect_match():
    user_skills = ["Python", "SQL", "Docker"]
    job_skills = ["PYTHON", "SQL", "DOCKER"]
    
    result = JobMatcher.calculate_match(user_skills, job_skills)
    
    assert result["match_percentage"] == 100.0
    assert sorted(result["matching_skills"]) == ["DOCKER", "PYTHON", "SQL"]
    assert result["missing_skills"] == []

def test_job_matcher_partial_match_and_gaps():
    user_skills = ["Python", "Git"]
    job_skills = ["PYTHON", "SQL", "DOCKER", "GIT"]
    
    result = JobMatcher.calculate_match(user_skills, job_skills)
    
    assert result["match_percentage"] == 50.0
    assert sorted(result["matching_skills"]) == ["GIT", "PYTHON"]
    assert sorted(result["missing_skills"]) == ["DOCKER", "SQL"]

def test_job_matcher_empty_inputs():
    # Test when user skills are empty
    result_no_user = JobMatcher.calculate_match([], ["PYTHON", "SQL"])
    assert result_no_user["match_percentage"] == 0.0
    assert result_no_user["matching_skills"] == []
    assert sorted(result_no_user["missing_skills"]) == ["PYTHON", "SQL"]

    # Test when job skills are empty
    result_no_job = JobMatcher.calculate_match(["PYTHON"], [])
    assert result_no_job["match_percentage"] == 100.0
    assert result_no_job["matching_skills"] == []
    assert result_no_job["missing_skills"] == []