import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.scrapers.spiders.linkedin_spider import LinkedInSpider
from src.scrapers.spiders.myfuturejobs_spider import MyFutureJobsSpider
from src.scrapers.spiders.remoteok_spider import RemoteOKSpider

def test_linkedin_spider_fallback():
    spider = LinkedInSpider()
    listings = spider._get_fallback_listings("software engineer")
    
    assert isinstance(listings, list)
    assert len(listings) > 0
    assert "title" in listings[0]
    assert "skills" in listings[0]
    assert "salary_range" in listings[0]
    assert "PYTHON" in listings[0]["skills"]

def test_myfuturejobs_spider_fallback():
    spider = MyFutureJobsSpider()
    listings = spider._get_fallback_listings("python developer")
    
    assert isinstance(listings, list)
    assert len(listings) > 0
    assert "title" in listings[0]
    assert "skills" in listings[0]
    assert "salary_range" in listings[0]
    assert "PYTHON" in listings[0]["skills"]

def test_remoteok_spider_integration():
    spider = RemoteOKSpider()
    # Verify the spider correctly instantiates the extractor and handles parsing logic
    assert hasattr(spider, "extractor")
    parsed = spider.extractor.parse_job("Remote Python and DuckDB backend developer needed. Salary: $5,000 - $8,000")
    
    assert "PYTHON" in parsed["skills"]
    assert "DUCKDB" in parsed["skills"]