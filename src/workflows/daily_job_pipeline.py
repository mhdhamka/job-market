import sys
from pathlib import Path
from prefect import flow, task

sys.path.append(str(Path(__file__).resolve().parents[1]))

from database.connection import get_connection, init_db
from scrapers.spiders.myfuturejobs_spider import MyFutureJobsSpider

@task(name="Initialize Database")
def setup_database():
    init_db()
    print("Database and tables verified.")

@task(name="Scrape and Process Job Postings")
def run_extraction_pipeline():
    # Instantiate the spider to pull live listings (with fallback resilience)
    spider = MyFutureJobsSpider()
    scraped_jobs = spider.fetch_jobs("python developer")
    
    con = get_connection(read_only=False)
    
    processed_count = 0
    # Loop through scraped entries and insert into DuckDB warehouse
    for i, job in enumerate(scraped_jobs, start=301):
        con.execute("""
            INSERT INTO job_listings (id, title, skills, salary_range)
            VALUES (?, ?, ?, ?)
        """, [i, job["title"], job["skills"], job["salary_range"]])
        
        processed_count += 1
        print(f"Processed & Stored: {job['title']} -> Skills: {job['skills']}")

    con.close()
    return f"Successfully processed and stored {processed_count} jobs from live pipeline."

@flow(name="Daily Job Market Intelligence Pipeline")
def daily_pipeline():
    setup_database()
    result = run_extraction_pipeline()
    print(result)

if __name__ == "__main__":
    # Run the flow locally
    daily_pipeline()