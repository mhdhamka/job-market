import requests
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from processing.extractor import JobExtractor

class RemoteOKSpider:
    def __init__(self):
        self.api_url = "https://remoteok.com/api"
        self.extractor = JobExtractor()

    def fetch_jobs(self, limit: int = 5):
        print("Fetching remote listings from RemoteOK API...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            response = requests.get(self.api_url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to reach RemoteOK API. Status code: {response.status_code}")
                return []

            data = response.json()
            
            # The first element in RemoteOK's JSON array is legal/metadata text, so we skip it
            job_entries = data[1:] if len(data) > 1 else []
            
            scraped_jobs = []
            for item in job_entries[:limit]:
                title = item.get('position', 'Unknown Title')
                description = item.get('description', '')
                
                # Parse through your robust regex JobExtractor
                parsed_data = self.extractor.parse_job(description)
                
                scraped_jobs.append({
                    "title": title,
                    "skills": parsed_data["skills"],
                    "salary_range": parsed_data["salary_range"] if parsed_data["salary_range"] != "Not Specified" else "Global/Remote Rate"
                })
                
            print(f"Successfully scraped {len(scraped_jobs)} jobs from RemoteOK.")
            return scraped_jobs

        except Exception as e:
            print(f"Error connecting to RemoteOK: {e}")
            return []

if __name__ == "__main__":
    spider = RemoteOKSpider()
    jobs = spider.fetch_jobs(3)
    print("RemoteOK Results:", jobs)