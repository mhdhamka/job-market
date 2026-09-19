import re
import numpy as np
from src.processing.cleaner import TextCleaner

class JobExtractor:
    def __init__(self):
        self.target_skills = [
            # Programming Languages (Including broader languages & scripting)
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'go', 'golang', 
            'scala', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'sql', 'bash', 'shell',

            # Data Engineering, AI & Big Data
            'spark', 'kafka', 'airflow', 'prefect', 'dbt', 'duckdb', 'snowflake', 'bigquery', 
            'redshift', 'pandas', 'numpy', 'hadoop', 'hive', 'etl', 'pytorch', 'tensorflow', 
            'langchain', 'openai', 'llm', 'scikit-learn',

            # Databases & Caching
            'postgresql', 'mysql', 'mongodb', 'redis', 'cassandra', 'elasticsearch', 'sqlite', 
            'dynamodb', 'oracle',

            # Cloud, DevOps & Infrastructure
            'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'terraform', 'ci/cd', 'git', 
            'linux', 'cloud', 'ansible', 'jenkins', 'github actions', 'prometheus', 'grafana',

            # Backend, Frontend & Mobile Frameworks
            'fastapi', 'flask', 'django', 'spring boot', 'node.js', 'express', 'react', 
            'next.js', 'angular', 'vue', 'nuxt.js', 'laravel', 'flutter', 'react native'
        ]

    def extract_skills(self, text: str) -> list:
        if not text:
            return []
        
        # Handle case where text might accidentally be a numpy array or non-string sequence
        if isinstance(text, np.ndarray):
            text = " ".join(str(item) for item in text.flatten())
        elif not isinstance(text, str):
            text = str(text)

        # Clean text to strip HTML tags and decode entities before matching
        text = TextCleaner.clean_text(text)

        text_lower = text.lower()
        found = [
            skill.upper() for skill in self.target_skills 
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower)
        ]
        
        # Ensure native python list is returned (safeguard against any numpy/set serialization issues)
        unique_skills = list(set(found))
        return [str(s) for s in unique_skills]

    def extract_salary(self, text: str) -> str:
        if not text:
            return "Not Specified"
            
        if isinstance(text, np.ndarray):
            text = " ".join(str(item) for item in text.flatten())
        elif not isinstance(text, str):
            text = str(text)

        # Clean text to strip HTML tags and decode entities before regex search
        text = TextCleaner.clean_text(text)

        text_lower = text.lower()
        # Matches patterns like RM 3,500 - RM 5,000 or RM3500-5000
        salary_match = re.search(r'rm\s*[\d,]+\s*(?:-\s*rm?\s*[\d,]+)?', text_lower)
        return str(salary_match.group(0).upper()) if salary_match else "Not Specified"

    def parse_job(self, raw_text: str) -> dict:
        skills = self.extract_skills(raw_text)
        
        # Final explicit check to convert numpy arrays if they exist in output dictionary
        if isinstance(skills, np.ndarray):
            skills = skills.tolist()

        return {
            "skills": skills,
            "salary_range": self.extract_salary(raw_text)
        }