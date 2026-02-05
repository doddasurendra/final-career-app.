import streamlit as st
import os

st.set_page_config(page_title="AI Career Assistant", page_icon="🚀", layout="wide")

try:
    from utils.sidebar_manager import render_sidebar
    render_sidebar()
except:
    st.sidebar.warning("Sidebar loading...")

st.title("🚀 Your AI Career Launchpad")
st.markdown("<div style='background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem;'><h2 style='color: white; margin:0;'>Get Hired Faster & Smarter.</h2></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

def safe_link(path, label, icon):
    if os.path.exists(path): st.page_link(path, label=label, icon=icon)
    else: st.info(f"Setting up {label}...")

with col1:
    st.info("👤 **Smart Profile**")
    safe_link("pages/1_Profile.py", "Manage Profile", "📂")
with col2:
    st.success("💼 **Job Aggregator**")
    safe_link("pages/2_Jobs.py", "Find Jobs", "🔍")
with col3:
    st.warning("📊 **Auto-Tracker**")
    safe_link("pages/3_Dashboard.py", "View Dashboard", "📊")
