import streamlit as st
from utils.data_manager import load_user_data
import base64
from io import BytesIO
from PIL import Image

def render_sidebar():
    with st.sidebar:
        user_data = load_user_data()
        
        # Profile Pic Logic
        if user_data and user_data.get("profile_pic"):
            try:
                image_data = base64.b64decode(user_data["profile_pic"])
                image = Image.open(BytesIO(image_data))
                st.image(image, width=120)
            except:
                st.image("https://cdn-icons-png.flaticon.com/512/1782/1782119.png", width=100)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/1782/1782119.png", width=100)

        st.title("Antigravity")
        st.caption("Your AI Career Companion")
        
        # Notification Badge
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
            
        unread_count = sum(1 for n in st.session_state.notifications if not n['read'])
        if unread_count > 0:
            st.metric("🔔 Notifications", f"{unread_count} New")
        else:
            st.caption("🔔 No new notifications")
            
        st.markdown("---")
        
        # Navigation shortcuts (optional, Streamlit handles pages automatically, but this adds flavor)
        if user_data:
            st.success(f"Hi, {user_data.get('name', 'User').split(' ')[0]}!")
            completion = user_data.get('profile_completion', 0)
            st.progress(completion / 100, text=f"Profile: {completion}%")
