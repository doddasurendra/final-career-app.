import streamlit as st
import os

# Page Config
st.set_page_config(page_title="AI Career Assistant", page_icon="🚀", layout="wide")

# Sidebar
from utils.sidebar_manager import render_sidebar
render_sidebar()

st.title("🚀 Your AI Career Launchpad")

st.markdown("""
<div style='background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;'>
    <h2 style='color: white; margin:0;'>Get Hired Faster & Smarter.</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.info("👤 **Smart Profile**")
    st.page_link("pages/1_Profile.py", label="Manage Profile", icon="📂")

with col2:
    st.success("💼 **Job Aggregator**")
    st.page_link("pages/2_Jobs.py", label="Find Jobs", icon="🔍")

with col3:
    st.warning("📈 **Auto-Tracker**")
    st.page_link("pages/3_Dashboard.py", label="View Dashboard", icon="📊")
