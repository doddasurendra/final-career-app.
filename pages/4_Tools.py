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

with tab1:
    st.header("Resume Optimizer")
    jd = st.text_area("Paste Job Description")
    if st.button("Analyze"):
        st.success("ATS Score: 85/100")
        st.write("Keywords found: Python, SQL, Project Management")

with tab2:
    st.header("Cover Letter Generator")
    role = st.text_input("Job Role")
    company = st.text_input("Company")
    if st.button("Generate"):
        st.code(f"Dear Hiring Manager,\n\nI am excited to apply for the {role} role at {company}...")
