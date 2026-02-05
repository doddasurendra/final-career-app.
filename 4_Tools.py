import streamlit as st
from utils.data_manager import load_user_data

# Setup
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

st.title("🛠️ Career Tools")

tab1, tab2 = st.tabs(["📄 Resume Optimizer", "✍️ Cover Letter Generator"])

user_data = load_user_data()

with tab1:
    st.header("Resume Optimizer")
    st.caption("Compare your resume against a Job Description (JD) to get an ATS Score.")
    
    col1, col2 = st.columns(2)
    with col1:
        jd = st.text_area("Paste Job Description here", height=300, placeholder="Copy-paste the JD...")
    
    with col2:
        current_resume = user_data.get('resume_text', "") if user_data else ""
        resume_text = st.text_area("Your Resume Text (Extracted)", value=current_resume, height=300)

    if st.button("Analyze Resume"):
        if jd and resume_text:
            # Mock Analysis
            keywords = jd.split()
            found = [k for k in keywords if k in resume_text]
            score = min(int((len(found) / len(keywords)) * 100) + 40, 95) # Fake logic for demo
            
            st.markdown(f"### 🎯 ATS Score: {score}/100")
            st.progress(score/100)
            
            if score < 70:
                st.warning("Needs Improvement")
            else:
                st.success("Great Match!")
                
            st.markdown("#### 🔑 Missing Keywords")
            missing = list(set(keywords) - set(found))
            # Just show some random missing "keywords" for demo logic correctness if real analysis was done
            st.write("Consider adding these keywords if you have the skills: " + ", ".join(missing[:5]) + "...")
        else:
            st.error("Please provide both Job Description and Resume Text.")

with tab2:
    st.header("Cover Letter Generator")
    st.caption("Generate a personalized cover letter in seconds.")
    
    with st.form("cl_form"):
        cl_company = st.text_input("Company Name")
        cl_role = st.text_input("Job Role")
        cl_manager = st.text_input("Hiring Manager Name (Optional)")
        
        generate = st.form_submit_button("Generate Cover Letter")
        
    if generate and cl_company and cl_role:
        name = user_data.get('name', '[Your Name]') if user_data else '[Your Name]'
        skills = ", ".join(user_data.get('skills', ['Java', 'Python'])) if user_data else "Java and Python"
        
        cl_content = f"""
Dear {cl_manager if cl_manager else 'Hiring Manager'},

I am writing to express my strong interest in the {cl_role} position at {cl_company}. As a 2026 Computer Science graduate with expertise in {skills}, I am excited about the opportunity to contribute to your engineering team.

I have followed {cl_company}'s work in the tech space and admire your innovative approach. During my academic projects, I have honed my skills in software development and problem-solving, which I believe align perfectly with the requirements of this role.

I am eager to bring my technical skills and passion for learning to {cl_company}. Thank you for considering my application. I look forward to the possibility of discussing how I can contribute to your team.

Sincerely,
{name}
        """
        st.text_area("Generated Cover Letter", value=cl_content, height=400)
        st.download_button("Download as Text", cl_content, file_name=f"Cover_Letter_{cl_company}.txt")
