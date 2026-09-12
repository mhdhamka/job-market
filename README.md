# Job Market Intelligence Engine

---

# Project Structure 

```text
job-market-intelligence/
│
├── .env.example                # Template for environment variables
├── .gitignore                  # Ignore venv, DuckDB files, logs, cache
├── README.md                   # Project overview and setup instructions
├── requirements.txt            # Python dependencies
│
├── data/
│   └── job_market.duckdb       # Local DuckDB database file (git-ignored)
│
├── notebooks/                  # Jupyter notebooks for prototyping & EDA
│   └── exploratory_analysis.ipynb
│
├── src/                        # Core application source code
│   │
│   ├── scrapers/               # Web scraping module
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   └── spiders/
│   │       ├── __init__.py
│   │       ├── myfuturejobs_spider.py
│   │       ├── linkedin_spider.py
│   │       └── remoteok_spider.py
│   │
│   ├── processing/             # Data cleaning & NLP/Regex extraction
│   │   ├── __init__.py
│   │   ├── cleaner.py
│   │   └── extractor.py
│   │
│   ├── database/               # Data warehouse layer
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── schemas.py
│   │
│   ├── workflows/              # Pipeline orchestration (Prefect/Airflow)
│   │   ├── __init__.py
│   │   └── daily_job_pipeline.py
│   │
│   ├── api/                    # FastAPI backend service
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes.py
│   │
│   └── dashboard/              # Streamlit frontend
│       ├── __init__.py
│       └── app.py
│
└── tests/                      # Automated tests
    ├── __init__.py
    ├── test_extractor.py
    └── test_api.py
```

---
