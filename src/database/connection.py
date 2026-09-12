import duckdb
from pathlib import Path

# Resolve path relative to project root or use default
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "job_market.duckdb"

def get_connection(read_only: bool = False):
    """Creates and returns a connection to the local DuckDB database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # If read-only is requested but the database file doesn't exist yet,
    # fallback to read-write so DuckDB can initialize the file safely.
    if read_only and not DB_PATH.exists():
        read_only = False
        
    return duckdb.connect(database=str(DB_PATH), read_only=read_only)

def init_db():
    """Initializes required tables and ensures all columns exist if they don't already."""
    con = get_connection(read_only=False)
    con.execute("""
        CREATE TABLE IF NOT EXISTS job_listings (
            id INTEGER,
            title VARCHAR,
            source VARCHAR,
            location VARCHAR,
            skills VARCHAR[],
            salary_range VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Safely add columns if running against an older existing schema
    try:
        con.execute("ALTER TABLE job_listings ADD COLUMN source VARCHAR;")
    except Exception:
        pass  # Column already exists
        
    try:
        con.execute("ALTER TABLE job_listings ADD COLUMN location VARCHAR;")
    except Exception:
        pass  # Column already exists

    con.close()

def get_next_id() -> int:
    """Dynamically calculates the next available primary key ID based on existing records."""
    con = get_connection(read_only=True)
    try:
        result = con.execute("SELECT MAX(id) FROM job_listings").fetchone()
        max_id = result[0] if result and result[0] is not None else 0
        return max_id + 1
    except Exception:
        # Fallback start ID if table is empty or doesn't exist yet
        return 1
    finally:
        con.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized successfully at: {DB_PATH}")