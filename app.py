import streamlit as st
import sys
import os

# Ensure the current directory is in the path for module imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from PIL import Image
from utils.data_manager import load_user_data

# Page Config (MUST BE FIRST)
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("assets/style.css")
except FileNotFoundError:
    st.warning("CSS file not found. Styles might be missing.")

# Sidebar
from utils.sidebar_manager import render_sidebar
render_sidebar()

# Main Content
st.title("🚀 Your AI Career Launchpad")
st.markdown("""
<div style='background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;'>
    <h2 style='color: white; margin:0;'>Get Hired Faster & Smarter.</h2>
    <p style='color: white; opacity: 0.9; margin-top: 0.5rem;'>
        Your personal AI agent for job matching, resume optimization, and application tracking.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="job-card">
        <h3>📄 Smart Profile</h3>
        <p>Build a 2026-ready profile that passes ATS checks automatically.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Profile.py", label="Manage Profile", icon="👤")

with col2:
    st.markdown("""
    <div class="job-card">
        <h3>🔍 Job Aggregator</h3>
        <p>One search for LinkedIn, Naukri, Indeed & more. No spam.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Jobs.py", label="Find Jobs", icon="💼")

with col3:
    st.markdown("""
    <div class="job-card">
        <h3>📊 Auto-Tracker</h3>
        <p>Track every application status in one Kanban-style board.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Dashboard.py", label="View Dashboard", icon="📈")

st.markdown("---")
st.caption("AI Career Assistant v1.0 | Built for Freshers")
