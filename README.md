
<div align="center">

# Job Market Intelligence Engine

> Automated Job Scraper, NLP Extractor, Data Warehouse, and Interactive Analytics Dashboard

[Documentation](./docs) · [Report Bug](https://github.com/mhdhamka/job-market-intelligence/issues) · [Request Feature](https://github.com/mhdhamka/job-market-intelligence/issues)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-Database-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Scrapy](https://img.shields.io/badge/Scrapy-Web%20Scraping-121212?style=for-the-badge&logo=scrapy&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

</div>

---

# Overview

An end-to-end data pipeline and intelligence platform designed to scrape, process, analyze, and serve live job market data. Built with a modular architecture, the system automates web harvesting across platforms (such as MYFutureJobs, LinkedIn, and RemoteOK), performs natural language processing (NLP) and regex extraction for skills and salaries, stores structured analytics in a lightning-fast local data warehouse, and exposes insights via a FastAPI backend and a Streamlit dashboard.

---

## Key Features

* **Multi-Platform Scrapers:** Automated Scrapy spiders targeting portal listings like MYFutureJobs, LinkedIn, and RemoteOK.
* **Smart Information Extraction:** NLP and regex cleaning pipelines to parse unstructured job descriptions into structured skill sets, salary ranges, and metadata.
* **Embedded Analytics Warehouse:** Powered by DuckDB for high-performance analytical queries without requiring heavy database server infrastructure.
* **RESTful API Service:** Built with FastAPI to serve job market data, metrics, and search queries with high performance and automatic documentation.
* **Interactive Dashboard:** A Streamlit-powered user interface to visualize job trends, salary distributions, and in-demand skills.
* **Robust CI/CD Testing:** Fully automated test suites using `pytest` and GitHub Actions ensuring code health and endpoint reliability.

---

## The Technology Stack

| Component | Technology | Description & Responsibilities |
| :--- | :--- | :--- |
| **Web Scraping** | Scrapy | Extracts raw job listings, descriptions, and metadata from target sites. |
| **Processing & NLP** | Python (Regex / SpaCy / Custom Parsers) | Cleans and extracts granular details like required skills, experience levels, and compensation. |
| **Data Warehouse** | DuckDB | Embedded columnar database for rapid analytical queries and storage. |
| **Backend API** | FastAPI, Uvicorn | High-performance asynchronous API serving job listings and metadata. |
| **Frontend / Dashboard** | Streamlit | Interactive data visualization and exploration interface. |
| **Workflow & Testing** | Pytest, GitHub Actions | Automated test runner and continuous integration pipeline. |

---

## Getting Started Locally

To run the complete Job Market Intelligence stack locally, follow these steps to set up your environment and dependencies.

### 1. Environment & Dependencies Setup
```bash
# Clone the repository
git clone https://github.com/mhdhamka/job-market.git
cd job-market

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Running Services

#### Run the FastAPI Backend

```bash
uvicorn src.api.main:app --reload --port 8000

```

#### Launch the Streamlit Dashboard

```bash
streamlit run src/dashboard/app.py

```

#### Run Automated Tests

```bash
pytest tests/

```

---

## Project Structure

```text
job-market/
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

# Contributing

Contributions are always welcome! If you'd like to improve this project, please follow these steps:

* Fork the Repository
* Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
* Commit your Changes (`git commit -m "add: some amazing feature"`)
* Push to the Branch (`git push origin feature/AmazingFeature`)
* Open a Pull Request

---

If you found this project interesting, consider giving it a star!

Made with ❤️ by mdhamka