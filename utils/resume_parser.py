import pdfplumber

def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            return "\n".join(p.extract_text() for p in pdf.pages)
    except: return ""

def extract_skills_from_text(text):
    skills = ["Python", "Java", "SQL", "React", "Node", "AWS", "Git"]
    return [s for s in skills if s.lower() in text.lower()]
