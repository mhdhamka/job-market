import duckdb
from pathlib import Path

# Resolve path relative to project root or use default
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "job_market.duckdb"

def get_connection(read_only: bool = False):
    """Creates and returns a connection to the local DuckDB database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(database=str(DB_PATH), read_only=read_only)

def init_db():
    """Initializes required tables if they don't already exist."""
    con = get_connection(read_only=False)
    con.execute("""
        CREATE TABLE IF NOT EXISTS job_listings (
            id INTEGER,
            title VARCHAR,
            skills VARCHAR[],
            salary_range VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized successfully at: {DB_PATH}")