## Architecture

### Tech Stack

| Component | Technology | Description & Responsibilities |
| :--- | :--- | :--- |
| **Browser Extension** | Plasmo, React, TypeScript | Injects floating tracker buttons into job portals to capture application metadata. | seriously only use this if you want to track you own job or else just ignore it.
| **Web Scraping** | Scrapy | Extracts raw job listings, descriptions, and metadata from target sites. |
| **Processing & NLP** | Python (Regex / SpaCy / Custom Parsers) | Cleans and extracts granular details like required skills, experience levels, and compensation. |
| **Data Warehouse** | DuckDB | Embedded columnar database for rapid analytical queries and storage. |
| **Backend API** | FastAPI, Uvicorn | High-performance asynchronous API serving job listings and metadata. |
| **Frontend / Dashboard** | Streamlit | Interactive data visualization and exploration interface. |
| **Workflow & Testing** | Pytest, GitHub Actions | Automated test runner and continuous integration pipeline. |

---

### Project Structure

```text
kerja-scraper/
│
├── .env.example                # Template for environment variables
├── .gitignore                  # Ignore venv, DuckDB files, logs, cache
├── README.md                   # Project overview and setup instructions
├── requirements.txt            # Python dependencies
│
├── data/
│   └── job_market.duckdb       # Local DuckDB database file (git-ignored)
|
├── extension/                  # Plasmo Browser Extension (Job Tracker)
│   ├── package.json            # Node dependencies (React/TypeScript)
│   ├── tsconfig.json           # TypeScript configuration
│   └── src/
│       ├── popup.tsx           # Extension popup interface
│       ├── content.ts          # Content script injected into JobStreet / MYFutureJobs
│       └── background.ts       # Service worker
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
│   │       ├── indeed_spider.py
│   │       ├── jobstreet_spider.py
│   │       ├── linkedin_spider.py
│   │       ├── myfuturejobs_spider.py
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
    ├── test_api.py
    ├── test_cleaner.py
    ├── test_extractor.py
    ├── test_matcher.py
    └── test_spiders.py

```

---