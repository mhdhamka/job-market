class JobMatcher:
    @staticmethod
    def calculate_match(user_skills: list, job_skills: list) -> dict:
        """
        Compares a list of user skills against a job's required skills.
        Returns match percentage, matching skills, and missing skills (skill gap).
        """
        if not user_skills:
            user_skills = []
        if not job_skills:
            job_skills = []

        # Normalize skills to uppercase for robust comparison
        user_set = {str(s).strip().upper() for s in user_skills if s}
        job_set = {str(s).strip().upper() for s in job_skills if s}

        if not job_set:
            return {
                "match_percentage": 100.0,
                "matching_skills": [],
                "missing_skills": []
            }

        matching_skills = sorted(list(user_set.intersection(job_set)))
        missing_skills = sorted(list(job_set.difference(user_set)))
        
        match_percentage = round((len(matching_skills) / len(job_set)) * 100.0, 2)

        return {
            "match_percentage": match_percentage,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills
        }

if __name__ == "__main__":
    # Quick test
    user = ["Python", "SQL", "Docker"]
    job = ["PYTHON", "FASTAPI", "SQL", "DOCKER", "AWS", "CLOUD"]
    
    result = JobMatcher.calculate_match(user, job)
    print("Match Results:", result)