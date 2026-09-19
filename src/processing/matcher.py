class JobMatcher:
    @staticmethod
    def calculate_match(user_skills, job_skills) -> dict:
        """
        Compares a list of user skills against a job's required skills.
        Returns match percentage, matching skills, and missing skills (skill gap).
        """
        # Safely handle None, NumPy arrays, or Pandas series for user_skills
        if user_skills is None or (hasattr(user_skills, "size") and user_skills.size == 0):
            user_skills = []
        elif not isinstance(user_skills, (list, set, tuple)):
            try:
                user_skills = list(user_skills)
            except Exception:
                user_skills = []

        # Safely handle None, NumPy arrays, or Pandas series for job_skills
        if job_skills is None or (hasattr(job_skills, "size") and job_skills.size == 0):
            job_skills = []
        elif not isinstance(job_skills, (list, set, tuple)):
            try:
                job_skills = list(job_skills)
            except Exception:
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