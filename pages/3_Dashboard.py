import streamlit as st
import pandas as pd
from utils.data_manager import load_user_data
from utils.notification_service import NotificationService
from utils.sidebar_manager import render_sidebar

# Setup
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except: pass

st.title("📊 Application Dashboard")
render_sidebar()

if 'applications' not in st.session_state:
    st.session_state.applications = [
        {"Company": "Google", "Role": "Software Engineer", "Status": "Applied"},
        {"Company": "Amazon", "Role": "SDE-1", "Status": "Interview"},
    ]

st.markdown("### 📋 Application Status")
st.table(st.session_state.applications)

st.markdown("### 📧 Notification Inbox")
notifier = NotificationService()
notifications = notifier.get_notifications()

if not notifications:
    st.info("No new notifications.")
else:
    for n in notifications:
        with st.expander(f"✉️ {n['subject']}"):
            st.write(n['body'])
            st.caption(f"Received at: {n['timestamp']}")
