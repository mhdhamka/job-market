
## Getting Started Locally

To run the complete Kerja Scraper stack locally, follow these steps to set up your environment and dependencies.

### 1. Environment & Dependencies Setup
```bash
# Clone the repository
git clone https://github.com/mhdhamka/kerja-scraper.git
cd kerja-scraper

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Run the Daily Job Pipeline (Data Ingestion)
```Bash
# Scrape and store initial job data into DuckDB
python src/workflows/daily_job_pipeline.py

```

### 3. Running Services

#### Run the FastAPI Backend

```bash
uvicorn src.api.main:app --reload --port 8000

```

#### Launch the Streamlit Dashboard

```bash
streamlit run src/dashboard/app.py

```
### 4. Installing the Plasmo Browser Extension
```Bash
# Navigate to extension directory
cd extension

# Install Node dependencies
npm install

# Build extension for development
npm run dev
```
Open your browser (Chrome/Edge), go to chrome://extensions/, enable Developer mode, click Load unpacked, and select the extension/build/chrome-mv3-dev directory.

#### Run Automated Tests

```bash
pytest tests/

```

---
