from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.database.connection import get_connection
from src.api.routes import router as api_router

app = FastAPI(
    title="Job Market Intelligence Engine",
    description="API for querying local DuckDB job market warehouse",
    version="1.0.0"
)

# Enable CORS for browser extension and local frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (safe for local development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes (e.g., /api/track, /api/analyze-job)
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Job Market Intelligence API! Go to /docs for interactive Swagger UI."}

@app.get("/jobs")
def get_jobs(limit: int = 10):
    con = get_connection(read_only=True)
    try:
        df = con.execute("SELECT * FROM job_listings LIMIT ?", [limit]).fetchdf()
        
        # Convert any NumPy arrays in the DataFrame to standard Python lists
        for col in df.columns:
            df[col] = df[col].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
            
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()