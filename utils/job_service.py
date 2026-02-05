import random
from faker import Faker

fake = Faker()

class JobService:
    def __init__(self):
        # We added your requested sites here!
        self.platforms = ["LinkedIn", "Naukri", "Internshala", "Indeed", "Glassdoor", "Wellfound"]
        self.roles = ["Software Engineer", "Frontend Developer", "Python Developer", "Data Scientist", "AI Engineer"]
        self.skills_pool = ["Python", "JavaScript", "SQL", "React", "AWS", "Git"]

    def generate_jobs(self, count=50):
        jobs = []
        for _ in range(count):
            role = random.choice(self.roles)
            platform = random.choice(self.platforms)
            jobs.append({
                "id": fake.uuid4(),
                "title": role,
                "company": fake.company(),
                "platform": platform,
                "location": random.choice(["Remote", "Bangalore", "Mumbai", "Pune", "Hyderabad"]),
                "salary": f"₹{random.randint(6, 25)} LPA",
                "requirements": random.sample(self.skills_pool, 3),
                "description": f"Exciting role at {fake.company()}...",
                "url": f"https://www.{platform.lower()}.com/jobs/{random.randint(1000, 9999)}"
            })
        return jobs

    def calculate_match_score(self, job_reqs, user_skills):
        if not user_skills: return 0
        matches = set(s.lower() for s in job_reqs).intersection(set(s.lower() for s in user_skills))
        return round((len(matches) / len(job_reqs)) * 100)
