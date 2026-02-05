import pdfplumber
import re

def extract_text_from_pdf(file):
    """
    Extracts text from a persistent filepath or a Streamlit UploadedFile object.
    
    Args:
        file: Either a string path or a Streamlit UploadedFile (BytesIO-like).
    
    Returns:
        str: Extracted text or empty string on failure.
    """
    try:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_skills_from_text(text, known_skills=None):
    """
    Simple keyword matching to find skills in text.
    """
    if known_skills is None:
        # Default list of popular CSE skills
        known_skills = [
            "Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL",
            "Machine Learning", "AI", "Data Science", "AWS", "Docker", "Git",
            "HTML", "CSS", "TypeScript", "Next.js", "Streamlit", "Figma"
        ]
    
    found_skills = []
    text_lower = text.lower()
    for skill in known_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
            
    return list(set(found_skills))
