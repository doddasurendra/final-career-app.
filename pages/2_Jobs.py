import streamlit as st
from utils.job_service import JobService
from utils.data_manager import load_user_data
from utils.sidebar_manager import render_sidebar

# Setup Styling
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

st.title("💼 Multi-Portal Search")
render_sidebar()

user_data = load_user_data()
user_skills = user_data.get("skills", []) if user_data else []
service = JobService()

# --- SEARCH BAR & FILTERS ---
st.markdown("### 🔍 Find Your Next Role")
col1, col2 = st.columns([2, 1])

with col1:
    search_query = st.text_input("", placeholder="Search Role or Company (e.g. Python)")
with col2:
    selected_sites = st.multiselect("🌐 Focus on Sites", service.platforms, default=service.platforms)

if 'jobs' not in st.session_state:
    st.session_state.jobs = service.generate_jobs(50)

# Filtering
filtered = [
    j for j in st.session_state.jobs 
    if j['platform'] in selected_sites and 
    (search_query.lower() in j['title'].lower() or search_query.lower() in j['company'].lower())
]

st.info(f"Showing {len(filtered)} jobs from your selected portals.")

# --- DISPLAY JOBS ---
for job in filtered:
    score = service.calculate_match_score(job["requirements"], user_skills)
    with st.container():
        st.markdown(f"""
        <div style="border:1px solid #e2e8f0; padding:15px; border-radius:12px; margin-bottom:15px; background: white; color: black; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between;">
                <h3 style="color: #1e293b; margin:0;">{job['title']}</h3>
                <span style="background: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{job['platform']}</span>
            </div>
            <p style="color: #64748b; margin: 5px 0;">{job['company']} • {job['location']} • <span style="color: #059669;">{job['salary']}</span></p>
            <div style="margin-top: 10px; font-size: 0.85rem;">Match Score: <b>{score}%</b></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Quick Apply", key=f"btn_{job['id']}"):
            st.success(f"Applied via {job['platform']}!")
