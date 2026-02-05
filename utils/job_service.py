import random
from faker import Faker

fake = Faker()

class JobService:
    def __init__(self):
        self.platforms = ["LinkedIn", "Naukri", "Indeed"]
        self.roles = ["Software Engineer", "Frontend Developer", "Python Developer"]
        self.skills_pool = ["Python", "JavaScript", "SQL", "React", "AWS"]

    def generate_jobs(self, count=20):
        jobs = []
        for _ in range(count):
            jobs.append({
                "id": fake.uuid4(),
                "title": random.choice(self.roles),
                "company": fake.company(),
                "platform": random.choice(self.platforms),
                "location": random.choice(["Remote", "Bangalore", "Mumbai"]),
                "salary": f"₹{random.randint(5, 15)} LPA",
                "requirements": random.sample(self.skills_pool, 3),
                "description": fake.paragraph()
            })
        return jobs

    def calculate_match_score(self, job_reqs, user_skills):
        if not user_skills: return 0
        matches = set(s.lower() for s in job_reqs).intersection(set(s.lower() for s in user_skills))
        return round((len(matches) / len(job_reqs)) * 100)
