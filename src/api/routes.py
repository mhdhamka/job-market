from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
import numpy as np
from typing import List

from src.processing.extractor import JobExtractor

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

@router.post("/analyze-job", response_model=JobResponseSchema)
def analyze_job_endpoint(payload: JobAnalyzeRequest):
    try:
        parsed_data = extractor.parse_job(payload.raw_text)
        return parsed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))