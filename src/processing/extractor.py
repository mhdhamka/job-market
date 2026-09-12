import re

class JobExtractor:
    def __init__(self):
        self.target_skills = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'golang', 'scala', 'sql',
            
            # Data Engineering & Big Data
            'spark', 'kafka', 'airflow', 'prefect', 'dbt', 'duckdb', 'snowflake', 'bigquery', 
            'redshift', 'pandas', 'numpy', 'hadoop', 'hive', 'etl',
            
            # Databases & Caching
            'postgresql', 'mysql', 'mongodb', 'redis', 'cassandra', 'elasticsearch', 'sqlite',
            
            # Cloud, DevOps & Infrastructure
            'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'terraform', 'ci/cd', 'git', 'linux', 'cloud',
            
            # Backend & Frontend Frameworks
            'fastapi', 'flask', 'django', 'spring boot', 'node.js', 'react', 'next.js', 'angular', 'vue', 'laravel'
        ]

    def extract_skills(self, text: str) -> list:
        if not text:
            return []
        text_lower = text.lower()
        found = [
            skill.upper() for skill in self.target_skills 
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower)
        ]
        return list(set(found)) # Remove duplicates

    def extract_salary(self, text: str) -> str:
        if not text:
            return "Not Specified"
        text_lower = text.lower()
        # Matches patterns like RM 3,500 - RM 5,000 or RM3500-5000
        salary_match = re.search(r'rm\s*[\d,]+\s*(?:-\s*rm?\s*[\d,]+)?', text_lower)
        return salary_match.group(0).upper() if salary_match else "Not Specified"

    def parse_job(self, raw_text: str) -> dict:
        return {
            "skills": self.extract_skills(raw_text),
            "salary_range": self.extract_salary(raw_text)
        }