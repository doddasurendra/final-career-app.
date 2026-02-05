import streamlit as st
import pandas as pd
from utils.job_service import JobService
from utils.data_manager import load_user_data
from utils.sidebar_manager import render_sidebar

# Setup
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

st.title("💼 Job Search Central")
render_sidebar()

user_data = load_user_data()
user_skills = user_data.get("skills", []) if user_data else []

service = JobService()

if 'jobs' not in st.session_state:
    st.session_state.jobs = service.generate_jobs(30)

for job in st.session_state.jobs:
    score = service.calculate_match_score(job["requirements"], user_skills)
    with st.container():
        st.markdown(f"""
        <div style="border:1px solid #e2e8f0; padding:15px; border-radius:10px; margin-bottom:10px;">
            <h3>{job['title']} @ {job['company']}</h3>
            <p><strong>Match Score: {score}%</strong> | {job['location']} | {job['salary']}</p>
            <p>{job['description'][:100]}...</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Apply to {job['company']}", key=f"btn_{job['id']}"):
            st.success(f"Application sent to {job['company']}!")
            st.toast("Check your Inbox for confirmation!", icon="📧")
