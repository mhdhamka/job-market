## Architecture

### System Overview & Data Flow

1. **Scrape & Capture:** Scrapy spiders collect job listings from target portals (Indeed, JobStreet, LinkedIn, MYFutureJobs, RemoteOK), while the optional Plasmo browser extension captures personal job applications when you want to track your own pipeline.
2. **Clean, Extract & Match:** Raw job text passes through `cleaner.py`, `extractor.py`, and `matcher.py` to normalize fields, extract skills and salary ranges, and score skill matches.
3. **Store & Serve:** Processed records are stored in a local DuckDB warehouse (`data/job_market.duckdb`) and surfaced via FastAPI endpoints, an interactive Streamlit dashboard, and automated daily workflows.

---

### Tech Stack

| Component | Technology | Description & Responsibilities |
| :--- | :--- | :--- |
| **Browser Extension** | Plasmo, React, TypeScript | Injects tracker UI into job portals to log personal job applications (optional; only needed if you want to track your own applications). |
| **Web Scraping** | Scrapy | Extracts raw job listings, descriptions, and metadata from target job boards. |
| **Processing & Matching** | Python (Regex / NLP / Custom Parsers) | Cleans text, extracts skills and salary ranges, and computes resume skill-match scores. |
| **Data Warehouse** | DuckDB | Embedded analytical database storing scraped job listings and tracked applications. |
| **Backend API** | FastAPI, Uvicorn | Asynchronous REST API serving job listings, analytics, and match endpoints. |
| **Frontend / Dashboard** | Streamlit, Plotly | Interactive dashboard for exploring job feeds, skill demand, and application status. |
| **Workflow & CI** | Python Workflows, Pytest, GitHub Actions | Runs scheduled/manual scraping pipelines, automated tests, and extension builds. |

---

### Project Structure

```text
kerja-scraper/
├── .env.example                    # Template for environment variables
├── .gitignore                      # Ignored build artifacts, caches, and local files
├── README.md                       # Project overview and quick links
├── requirements.txt                # Python dependencies
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI test, extension build, and daily scrape workflow
│
├── data/
│   └── job_market.duckdb           # Local DuckDB database file
│
├── docs/
│   ├── ARCHITECTURE.md             # System architecture and project structure
│   ├── GETTING_STARTED.md          # Setup, running spiders, API, and dashboard guide
│   └── notebooks/
│       └── exploratory_analysis.ipynb
│
├── extension/                      # Optional Plasmo Browser Extension (Personal Tracker)
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── assets/
│   │   └── icon.png
│   └── src/
│       ├── background.ts           # Extension background service worker
│       ├── content.ts            # Content script for job portal pages
│       └── popup.tsx             # Extension popup UI
│
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI application entrypoint
│   │   └── routes.py             # API route handlers
│   ├── dashboard/
│   │   ├── __init__.py
│   │   └── app.py                # Streamlit intelligence and tracker dashboard
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py         # DuckDB connection and initialization helpers
│   │   └── schemas.py            # Table definitions and schema setup
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── cleaner.py            # Text normalization and cleaning utilities
│   │   ├── extractor.py          # Skill, metadata, and salary extraction
│   │   └── matcher.py            # Resume skill-matching logic
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── items.py              # Scrapy item models
│   │   ├── middlewares.py        # Request/response middlewares
│   │   ├── pipelines.py          # Item processing and persistence pipelines
│   │   └── spiders/
│   │       ├── __init__.py
│   │       ├── indeed_spider.py
│   │       ├── jobstreet_spider.py
│   │       ├── linkedin_spider.py
│   │       ├── myfuturejobs_spider.py
│   │       └── remoteok_spider.py
│   └── workflows/
│       ├── __init__.py
│       └── daily_job_pipeline.py # End-to-end daily scrape and warehouse pipeline
│
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_cleaner.py
    ├── test_extractor.py
    ├── test_matcher.py
    └── test_spiders.py
    
```

---