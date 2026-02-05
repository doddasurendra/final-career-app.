import pandas as pd
import random
from faker import Faker

fake = Faker()

class JobService:
    def __init__(self):
        self.platforms = ["LinkedIn", "Naukri", "Indeed", "Internshala", "Glassdoor", "Wellfound", "SimplyHired"]
        self.roles = [
            "Software Engineer - Fresher", "Junior Python Developer", 
            "Frontend Developer (React)", "Data Analyst Intern", 
            "AI/ML Engineer - Entry Level", "Associate Software Developer",
            "Graduate Engineer Trainee", "Full Stack Developer", "Backend Developer"
        ]
        self.companies = [
            "Google", "Microsoft", "Amazon", "TCS", "Infosys", "Wipro", 
            "Accenture", "Zomato", "Swiggy", "Cred", "Zoho", "Freshworks",
            "Flipkart", "Tech Mahindra", "HCL Tech"
        ]
        self.skills_pool = [
            "Python", "Java", "C++", "React", "Node.js", "SQL", "AWS", 
            "Docker", "Machine Learning", "Data Structures", "Algorithms",
            "HTML", "CSS", "JavaScript", "TypeScript", "Next.js"
        ]

    def generate_jobs(self, count=50):
        jobs = []
        for _ in range(count):
            role = random.choice(self.roles)
            company = random.choice(self.companies)
            platform = random.choice(self.platforms)
            
            # Select 3-6 random requirements
            reqs = random.sample(self.skills_pool, k=random.randint(3, 6))
            
            job = {
                "id": fake.uuid4(),
                "title": role,
                "company": company,
                "platform": platform,
                "location": random.choice(["Remote", "Hybrid", "Bangalore", "Pune", "Hyderabad", "Mumbai", "Noida"]),
                "salary": f"₹{random.randint(4, 15)} LPA",
                "posted_days_ago": random.randint(0, 30),
                "requirements": reqs,
                "link": "#",
                "description": fake.paragraph(nb_sentences=5)
            }
            jobs.append(job)
        return jobs

    def calculate_match_score(self, job_reqs, user_skills):
        if not user_skills:
            return 0
        
        # Normalize
        job_reqs_set = set(s.lower() for s in job_reqs)
        user_skills_set = set(s.lower() for s in user_skills)
        
        matches = job_reqs_set.intersection(user_skills_set)
        
        # Basic overlap score
        score = (len(matches) / len(job_reqs_set)) * 100
        
        # Penalties/Bonuses can be added here
        return round(score)
