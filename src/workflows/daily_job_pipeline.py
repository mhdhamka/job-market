import sys
from pathlib import Path
from prefect import flow, task

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.database.connection import get_connection, init_db
from src.scrapers.spiders.myfuturejobs_spider import MyFutureJobsSpider
from src.scrapers.spiders.remoteok_spider import RemoteOKSpider
from src.scrapers.spiders.linkedin_spider import LinkedInSpider
from src.scrapers.spiders.jobstreet_spider import JobStreetSpider
from src.scrapers.spiders.indeed_spider import IndeedSpider

@task(name="Initialize Database")
def setup_database():
    init_db()
    print("Database and tables verified.")

@task(name="Scrape and Process Job Postings")
def run_extraction_pipeline():
    con = get_connection(read_only=False)
    processed_count = 0

    # Dynamically determine the starting ID to avoid primary key conflicts
    res = con.execute("SELECT MAX(id) FROM job_listings").fetchone()
    base_id = (res[0] if res and res[0] is not None else 0) + 1

    # 1. Fetch from Local Portal (MyFutureJobs)
    print("--- Running MyFutureJobs Spider ---")
    local_spider = MyFutureJobsSpider()
    local_jobs = local_spider.fetch_jobs("python developer")
    
    for job in local_jobs:
        con.execute("""
            INSERT INTO job_listings (id, title, source, location, skills, salary_range)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            base_id, 
            job.get("title"), 
            "MyFutureJobs", 
            job.get("location", "Malaysia"), 
            job.get("skills"), 
            job.get("salary_range")
        ])
        
        processed_count += 1
        base_id += 1
        print(f"Stored Local: {job.get('title')} -> Skills: {job.get('skills')}")

    # 2. Fetch from Global API (RemoteOK)
    print("--- Running RemoteOK Spider ---")
    global_spider = RemoteOKSpider()
    global_jobs = global_spider.fetch_jobs(limit=5)
    
    for job in global_jobs:
        con.execute("""
            INSERT INTO job_listings (id, title, source, location, skills, salary_range)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            base_id, 
            job.get("title"), 
            "RemoteOK", 
            job.get("location", "Global/Remote"), 
            job.get("skills"), 
            job.get("salary_range")
        ])
        
        processed_count += 1
        base_id += 1
        print(f"Stored Global: {job.get('title')} -> Skills: {job.get('skills')}")

    # 3. Fetch from LinkedIn
    print("--- Running LinkedIn Spider ---")
    linkedin_spider = LinkedInSpider()
    linkedin_jobs = linkedin_spider.fetch_jobs("software engineer", "Malaysia")
    
    for job in linkedin_jobs:
        con.execute("""
            INSERT INTO job_listings (id, title, source, location, skills, salary_range)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            base_id, 
            job.get("title"), 
            "LinkedIn", 
            job.get("location", "Malaysia"), 
            job.get("skills"), 
            job.get("salary_range")
        ])
        
        processed_count += 1
        base_id += 1
        print(f"Stored LinkedIn: {job.get('title')} -> Skills: {job.get('skills')}")

    # 4. Fetch from JobStreet
    print("--- Running JobStreet Spider ---")
    jobstreet_spider = JobStreetSpider()
    jobstreet_jobs = jobstreet_spider.fetch_jobs("software engineer", "malaysia")
    
    for job in jobstreet_jobs:
        con.execute("""
            INSERT INTO job_listings (id, title, source, location, skills, salary_range)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            base_id, 
            job.get("title"), 
            "JobStreet", 
            "Malaysia", 
            job.get("skills"), 
            job.get("salary_range")
        ])
        
        processed_count += 1
        base_id += 1
        print(f"Stored JobStreet: {job.get('title')} -> Skills: {job.get('skills')}")

    # 5. Fetch from Indeed
    print("--- Running Indeed Spider ---")
    indeed_spider = IndeedSpider()
    indeed_jobs = indeed_spider.fetch_jobs("software engineer", "Malaysia")
    
    for job in indeed_jobs:
        con.execute("""
            INSERT INTO job_listings (id, title, source, location, skills, salary_range)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            base_id, 
            job.get("title"), 
            "Indeed", 
            "Malaysia", 
            job.get("skills"), 
            job.get("salary_range")
        ])
        
        processed_count += 1
        base_id += 1
        print(f"Stored Indeed: {job.get('title')} -> Skills: {job.get('skills')}")

    con.close()
    return f"Successfully processed and stored {processed_count} jobs from multi-source pipeline (MyFutureJobs, RemoteOK, LinkedIn, JobStreet, Indeed)."

@flow(name="Daily Job Market Intelligence Pipeline")
def daily_pipeline():
    setup_database()
    result = run_extraction_pipeline()
    print(result)

if __name__ == "__main__":
    # Run the flow locally
    daily_pipeline()