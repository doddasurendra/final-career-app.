import streamlit as st
from utils.data_manager import load_user_data

def render_sidebar():
    with st.sidebar:
        st.title("Antigravity")
        user = load_user_data()
        if user:
            st.success(f"Hi, {user.get('name', 'User')}!")
            st.progress(user.get('profile_completion', 0) / 100)
        else:
            st.info("Complete your profile!")
