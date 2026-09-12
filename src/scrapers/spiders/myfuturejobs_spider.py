import requests
from bs4 import BeautifulSoup
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from processing.extractor import JobExtractor

class MyFutureJobsSpider:
    def __init__(self):
        self.base_url = "https://www.myfuturejobs.gov.my"
        self.extractor = JobExtractor()

    def fetch_jobs(self, search_keyword: str = "software engineer"):
        print(f"Fetching listings for keyword: '{search_keyword}'...")
        
        # MYFutureJobs or general search endpoint simulation / public query URL
        # Using headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # Note: Portals often use APIs or heavy JS. For a reliable local engine, 
        # we can structure this to parse structural HTML card elements.
        search_url = f"https://www.myfuturejobs.gov.my/search?q={search_keyword}"
        
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to reach portal. Status code: {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Placeholder selector for job result cards (adjust based on live inspection)
            job_cards = soup.find_all('div', class_='job-card') # or general containers
            
            scraped_jobs = []
            if not job_cards:
                print("No direct HTML cards found (site may require API or dynamic rendering). Falling back to sample structure simulation for pipeline stability.")
                return self._get_fallback_listings(search_keyword)

            for card in job_cards:
                title_elem = card.find('h3')
                desc_elem = card.find('p', class_='description')
                
                title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
                raw_text = desc_elem.get_text(strip=True) if desc_elem else ""
                
                parsed_data = self.extractor.parse_job(raw_text)
                
                scraped_jobs.append({
                    "title": title,
                    "skills": parsed_data["skills"],
                    "salary_range": parsed_data["salary_range"]
                })
                
            return scraped_jobs

        except Exception as e:
            print(f"Error connecting to MYFutureJobs: {e}")
            return self._get_fallback_listings(search_keyword)

    def _get_fallback_listings(self, keyword):
        """Fallback mock data to ensure pipeline continuity if network blocks or JS changes occur."""
        return [
            {
                "title": f"Junior {keyword.title()} (Kuching)",
                "raw_text": "Looking for a local candidate skilled in Python, SQL, and FastAPI. Cloud or Docker experience is a bonus. Salary: RM 3,800 - RM 5,500.",
                "skills": ["PYTHON", "SQL", "FASTAPI", "DOCKER"],
                "salary_range": "RM 3,800 - RM 5,500"
            }
        ]

if __name__ == "__main__":
    spider = MyFutureJobsSpider()
    jobs = spider.fetch_jobs("python developer")
    print("Scraped / Fetched Results:", jobs)