import streamlit as st
import pandas as pd
from utils.data_manager import load_user_data, save_user_data

# Setup
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

from utils.notification_service import NotificationService
from utils.sidebar_manager import render_sidebar

# Render Sidebar
render_sidebar()

st.title("📊 Application Dashboard")

# Initialize Mock Applications if needed
if 'applications' not in st.session_state:
    st.session_state.applications = [
        {"Company": "Google", "Role": "Software Engineer", "Date": "2024-02-01", "Status": "Applied", "Platform": "LinkedIn"},
        {"Company": "Amazon", "Role": "SDE-1", "Date": "2024-01-28", "Status": "Interview", "Platform": "Naukri"},
        {"Company": "Zomato", "Role": "Frontend intern", "Date": "2024-02-03", "Status": "Rejected", "Platform": "Internshala"},
    ]

# Merge with tracked jobs from Jobs page
if 'tracked_jobs' in st.session_state:
    for job in st.session_state.tracked_jobs:
        # Avoid duplicates based on simple title+company check
        exists = any(app['Company'] == job['company'] and app['Role'] == job['title'] for app in st.session_state.applications)
        if not exists:
            st.session_state.applications.append({
                "Company": job['company'], 
                "Role": job['title'], 
                "Date": "2024-02-05", # Today's date mock
                "Status": job.get('initial_status', 'Interested'),
                "Platform": job['platform']
            })
    st.session_state.tracked_jobs = [] # Clear tracked buffer

apps_df = pd.DataFrame(st.session_state.applications)

# Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Applications", len(apps_df))
col2.metric("Interviews", len(apps_df[apps_df['Status'] == 'Interview']))
col3.metric("Offers", len(apps_df[apps_df['Status'] == 'Offer']))
col4.metric("Pending", len(apps_df[apps_df['Status'].isin(['Applied', 'Interested'])]))

tab_status, tab_inbox = st.tabs(["📋 Status Board", "📧 Inbox (Notifications)"])

with tab_status:
    st.markdown("### 📋 Status Board")
    
    # Editable Data Editor
    edited_df = st.data_editor(
        apps_df,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                help="Update application status",
                width="medium",
                options=[
                    "Interested", "Applied", "Viewed", "Interview", "Offer", "Rejected", "Shortlisted"
                ],
                required=True,
            )
        },
        hide_index=True,
        num_rows="dynamic",
        use_container_width=True
    )
    
    # Sync changes back to session state
    if not edited_df.equals(apps_df):
        # Check for status changes to trigger notifications
        new_records = edited_df.to_dict('records')
        old_records = st.session_state.applications
        
        notifier = NotificationService()
        
        # Load user data only once
        from utils.data_manager import load_user_data
        ud = load_user_data() or {}
        u_email = ud.get('email')
        u_phone = ud.get('phone')
        
        for new, old in zip(new_records, old_records):
            if new['Status'] == 'Shortlisted' and old['Status'] != 'Shortlisted':
                if u_email:
                    notifier.send_shortlist_email(new, user_email=u_email)
                if u_phone:
                    notifier.send_sms(f"Congrats! Shortlisted by {new['Company']} for {new['Role']}.", phone=u_phone)
                st.toast(f"📱 Simulated SMS & 📧 Email logged to Inbox!", icon="🎉")
        
        st.session_state.applications = new_records
        st.rerun()

with tab_inbox:
    st.markdown("### 📧 Email Notifications")
    notifications = NotificationService().get_notifications()
    
    if not notifications:
        st.info("No new emails.")
    else:
        for email in notifications:
            with st.expander(f"{'🆕 ' if not email['read'] else ''}{email['subject']} - {email['timestamp']}"):
                st.markdown(email['body'])
                email['read'] = True

st.markdown("---")
st.markdown("### 📅 Upcoming Interviews")
interviews = [app for app in st.session_state.applications if app['Status'] == 'Interview']

if interviews:
    for i in interviews:
        st.info(f"🎤 Interview with **{i['Company']}** for **{i['Role']}** position. (Check email for schedule)")
else:
    st.caption("No upcoming interviews scheduled yet.")
