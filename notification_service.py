import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationService:
    def __init__(self):
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
            
    def _send_real_email(self, to_email, subject, body):
        """
        Sends a real email if secrets are configured.
        """
        try:
            if "email" in st.secrets:
                sender_email = st.secrets["email"]["sender_email"]
                password = st.secrets["email"]["app_password"]
                smtp_server = st.secrets["email"]["smtp_server"]
                smtp_port = st.secrets["email"]["smtp_port"]
                
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
                
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, password)
                    server.send_message(msg)
                return True
        except Exception as e:
            print(f"SMTP Error: {e}")
            return False
        return False

    def send_application_email(self, job, user_email=None):
        """
        Simulates sending an email for a job application.
        """
        if not user_email:
            user_email = "user@example.com"

        subject = f"Application Confirmed: {job['title']} at {job['company']}"
        body = f"""
        Sent to: {user_email}
        
        Dear Candidate,

        You have successfully applied for the following position:
        
        Role: {job['title']}
        Company: {job['company']}
        Location: {job['location']}
        Salary: {job['salary']}
        
        We will notify you if you are shortlisted.
        
        Best,
        {job['company']} HR Team
        """
        
        # Try real email
        is_sent = self._send_real_email(user_email, subject, body)
        
        # Log to internal system
        email = {
            "id": len(st.session_state.notifications) + 1,
            "type": "Application" + (" ✅ Sent" if is_sent else " (Mock)"),
            "subject": subject,
            "body": body,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "read": False
        }
        st.session_state.notifications.append(email)
        return True

    def send_shortlist_email(self, app_data, user_email=None):
        """
        Simulates sending an email when shortlisted.
        """
        if not user_email:
            user_email = "user@example.com"

        subject = f"🎉 Great News! You are Shortlisted by {app_data['Company']}"
        body = f"""
        Sent to: {user_email}
        
        Dear Candidate,

        Congratulations! Your application for {app_data['Role']} has been shortlisted.
        
        Next Steps:
        1. Our team will contact you for an interview.
        2. Please prepare your portfolio.
        
        Good luck!
        """
        
        # Try real email
        is_sent = self._send_real_email(user_email, subject, body)
        
        email = {
            "id": len(st.session_state.notifications) + 1,
            "type": "Shortlist" + (" ✅ Sent" if is_sent else " (Mock)"),
            "subject": subject,
            "body": body,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "read": False
        }
        st.session_state.notifications.append(email)
        return True

    def send_sms(self, message, phone=None):
        """
        Simulates sending an SMS.
        """
        if not phone:
            phone = "Unknown"
            
        sms = {
            "id": len(st.session_state.notifications) + 1,
            "type": f"SMS to {phone}",
            "subject": f"💬 SMS Alert",
            "body": f"MESSAGE: {message}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "read": False
        }
        st.session_state.notifications.append(sms)
        return True

    def get_notifications(self):
        return sorted(st.session_state.notifications, key=lambda x: x['timestamp'], reverse=True)
