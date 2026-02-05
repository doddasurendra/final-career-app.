import streamlit as st
from datetime import datetime

class NotificationService:
    def __init__(self):
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []

    def send_application_email(self, job, user_email="user@example.com"):
        notif = {
            "subject": f"Application Sent: {job['title']} @ {job['company']}",
            "body": f"Your application was successfully sent to {job['company']}.",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "read": False
        }
        st.session_state.notifications.append(notif)

    def get_notifications(self):
        return st.session_state.notifications
