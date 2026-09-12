from fastapi import FastAPI, HTTPException
import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.database.connection import get_connection

app = FastAPI(
    title="Job Market Intelligence Engine",
    description="API for querying local DuckDB job market warehouse",
    version="1.0.0"
)

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