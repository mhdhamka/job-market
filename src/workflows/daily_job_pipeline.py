import sys
from pathlib import Path
from prefect import flow, task

sys.path.append(str(Path(__file__).resolve().parents[1]))

from database.connection import get_connection, init_db
from scrapers.spiders.myfuturejobs_spider import MyFutureJobsSpider
from scrapers.spiders.remoteok_spider import RemoteOKSpider
from scrapers.spiders.linkedin_spider import LinkedInSpider

@task(name="Initialize Database")
def setup_database():
    init_db()
    print("Database and tables verified.")

@task(name="Scrape and Process Job Postings")
def run_extraction_pipeline():
    con = get_connection(read_only=False)
    processed_count = 0
    base_id = 401  # Starting ID offset for the new batch

    # 1. Fetch from Local Portal (MyFutureJobs)
    print("--- Running MyFutureJobs Spider ---")
    local_spider = MyFutureJobsSpider()
    local_jobs = local_spider.fetch_jobs("python developer")
    
    for job in local_jobs:
        con.execute("""
            INSERT INTO job_listings (id, title, skills, salary_range)
            VALUES (?, ?, ?, ?)
        """, [base_id, job["title"], job["skills"], job["salary_range"]])
        
        processed_count += 1
        base_id += 1
        print(f"Stored Local: {job['title']} -> Skills: {job['skills']}")

    # 2. Fetch from Global API (RemoteOK)
    print("--- Running RemoteOK Spider ---")
    global_spider = RemoteOKSpider()
    global_jobs = global_spider.fetch_jobs(limit=5)
    
    for job in global_jobs:
        con.execute("""
            INSERT INTO job_listings (id, title, skills, salary_range)
            VALUES (?, ?, ?, ?)
        """, [base_id, job["title"], job["skills"], job["salary_range"]])
        
        processed_count += 1
        base_id += 1
        print(f"Stored Global: {job['title']} -> Skills: {job['skills']}")

    # 3. Fetch from LinkedIn
    print("--- Running LinkedIn Spider ---")
    linkedin_spider = LinkedInSpider()
    linkedin_jobs = linkedin_spider.fetch_jobs("software engineer", "Malaysia")
    
    for job in linkedin_jobs:
        con.execute("""
            INSERT INTO job_listings (id, title, skills, salary_range)
            VALUES (?, ?, ?, ?)
        """, [base_id, job["title"], job["skills"], job["salary_range"]])
        
        processed_count += 1
        base_id += 1
        print(f"Stored LinkedIn: {job['title']} -> Skills: {job['skills']}")

    con.close()
    return f"Successfully processed and stored {processed_count} jobs from multi-source pipeline (MyFutureJobs, RemoteOK, LinkedIn)."

@flow(name="Daily Job Market Intelligence Pipeline")
def daily_pipeline():
    setup_database()
    result = run_extraction_pipeline()
    print(result)

if __name__ == "__main__":
    # Run the flow locally
    daily_pipeline()