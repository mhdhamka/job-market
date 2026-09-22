from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
import numpy as np
from typing import List, Optional

from src.processing.extractor import JobExtractor
from src.database.connection import get_connection, get_next_application_id

router = APIRouter()
extractor = JobExtractor()

class JobAnalyzeRequest(BaseModel):
    raw_text: str

class JobResponseSchema(BaseModel):
    skills: List[str]
    salary_range: str

    @field_validator('skills', mode='before')
    @classmethod
    def ensure_list_from_numpy(cls, v):
        """Safely converts numpy arrays or other sequences to a standard Python list."""
        if isinstance(v, np.ndarray):
            return v.tolist()
        if isinstance(v, set):
            return list(v)
        return v

class JobApplicationPayload(BaseModel):
    job_title: str
    company: str
    source_platform: str
    job_url: str
    status: Optional[str] = "Applied"
    salary_range: Optional[str] = "Not Specified"

@router.post("/analyze-job", response_model=JobResponseSchema)
def analyze_job_endpoint(payload: JobAnalyzeRequest):
    try:
        parsed_data = extractor.parse_job(payload.raw_text)
        return parsed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/track")
def track_job_application(payload: JobApplicationPayload):
    """Receives application payload from Plasmo extension and saves it to DuckDB."""
    con = get_connection(read_only=False)
    try:
        app_id = get_next_application_id()
        con.execute("""
            INSERT INTO job_applications (id, job_title, company, source_platform, job_url, status, salary_range)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            app_id,
            payload.job_title,
            payload.company,
            payload.source_platform,
            payload.job_url,
            payload.status,
            payload.salary_range
        ])
        return {
            "status": "success", 
            "message": "Job application tracked successfully!", 
            "id": app_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()