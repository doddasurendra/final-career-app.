import streamlit as st
import pandas as pd
from utils.job_service import JobService
from utils.data_manager import load_user_data

# Setup
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

st.title("💼 Job Search Central")
st.caption("Aggregated from LinkedIn, Naukri, Indeed, Glassdoor & more.")

# Load User Data for Matching
user_data = load_user_data()
user_skills = user_data.get("skills", []) if user_data else []

if not user_skills:
    st.warning("⚠️ Complete your profile to see Match Scores!")

from utils.sidebar_manager import render_sidebar

# Initialize Service
service = JobService()

# Render Global Sidebar
render_sidebar()

# Page-Specific Sidebar Filters
with st.sidebar:
    st.header("Search Filters")
    platforms = st.multiselect("Platforms", service.platforms, default=service.platforms[:3])
    job_type = st.multiselect("Job Mode", ["Remote", "Hybrid", "On-site"], default=["Remote", "Hybrid"])
    # min_salary moved to keep context if needed, but sidebar structure implies append
    min_salary = st.slider("Min Salary (LPA)", 3, 20, 6)
    
    st.markdown("---")
    st.markdown("### 🤖 Auto-Apply")
    
    # Configurable Threshold
    apply_threshold = st.slider("Minimum Match Score %", min_value=0, max_value=100, value=70, help="Apply to all jobs with a score above this value.")
    
    col_auto1, col_auto2 = st.columns(2)
    
    candidates = []
    run_auto = False
    
    with col_auto1:
        if st.button(f"Apply to Matches > {apply_threshold}%"):
             if 'jobs' in st.session_state:
                candidates = [j for j in st.session_state.jobs if j.get("match_score", 0) >= apply_threshold]
                run_auto = True

    with col_auto2:
        if st.button("🚨 Apply to ALL Jobs"):
            if 'jobs' in st.session_state:
                candidates = st.session_state.jobs # Select ALL
                run_auto = True
    
    if run_auto:
        if 'jobs' in st.session_state:
            
            if not candidates:
                st.warning(f"No jobs found to apply.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                applied_count = 0
                
                if 'tracked_jobs' not in st.session_state:
                    st.session_state.tracked_jobs = []
                    
                import time
                
                # Access applications to check for duplicates
                existing_apps = set()
                if 'applications' in st.session_state:
                    existing_apps = {(app['Company'], app['Role']) for app in st.session_state.applications}

                from utils.notification_service import NotificationService
                notifier = NotificationService()
                
                # Get Resumes
                resumes = user_data.get("resumes", [])

                for i, job in enumerate(candidates):
                    # Check if already applied
                    if (job['company'], job['title']) in existing_apps or job.get('initial_status') == 'Applied':
                        continue

                    # Simulate automation delay
                    status_text.text(f"Applying to {job['company']}...")
                    progress_bar.progress((i + 1) / len(candidates))
                    time.sleep(0.05) 
                    
                    # Update status in main job list so UI reflects it immediately
                    job['initial_status'] = 'Applied'
                    
                    # Select Best Resume
                    selected_resume_name = "Default Profile"
                    if resumes:
                        best_score = -1
                        best_resume = None
                        for res in resumes:
                            # Use existing matching logic but against resume skills
                            r_score = service.calculate_match_score(job["requirements"], res.get('skills', []))
                            if r_score > best_score:
                                best_score = r_score
                                best_resume = res
                        
                        if best_resume:
                            selected_resume_name = best_resume['filename']
                    
                    # Add to tracker
                    job_copy = job.copy()
                    job_copy['applied_resume'] = selected_resume_name # Track used resume
                    st.session_state.tracked_jobs.append(job_copy)
                    
                    # Send Notification
                    # We can pass the selected resume name to the notifier if we updated it, 
                    # for now just sending the job is enough as per req, but user asked to select correct resume.
                    
                    u_email = user_data.get('email')
                    u_phone = user_data.get('phone')
                    
                    if u_email:
                        notifier.send_application_email(job, user_email=u_email)
                    if u_phone:
                        notifier.send_sms(f"Applied to {job['company']} for {job['title']}.", phone=u_phone)
                        
                    st.toast(f"📧 Email logged\n📱 Simulated SMS logged to Dashboard", icon="✅")
                    
                    applied_count += 1
                
                status_text.text("Done!")
                if applied_count > 0:
                    st.toast(f"🚀 Applied to {applied_count} jobs!")
                    st.rerun() # Rerun to update button states
                else:
                    st.info("Already applied to all matching jobs.")

# Generate Jobs (Mock)
if 'jobs' not in st.session_state:
    st.session_state.jobs = service.generate_jobs(40)

jobs = st.session_state.jobs

# Apply Matching Logic
ranked_jobs = []
for job in jobs:
    score = service.calculate_match_score(job["requirements"], user_skills)
    job["match_score"] = score
    ranked_jobs.append(job)

# Sort by Match Score (Descending)
ranked_jobs.sort(key=lambda x: x["match_score"], reverse=True)

# Main Feed
for job in ranked_jobs:
    # Filter Checks
    if platforms and job["platform"] not in platforms:
        continue
    # Simple workaround for location filter logic mapping
    if "Remote" not in job_type and job["location"] == "Remote":
        continue
        
    score_color = "green" if job["match_score"] > 70 else "orange" if job["match_score"] > 40 else "red"
    
    with st.container():
        st.markdown(f"""
        <div class="job-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h3 style="margin:0; color:#eff6ff;">{job['title']}</h3>
                    <p style="margin:4px 0 8px 0; font-weight:600; color:#93c5fd;">{job['company']} • <span style="color:#cbd5e1;">{job['platform']}</span></p>
                </div>
                <div style="text-align: right;">
                    <span style="background-color: {score_color}; padding: 4px 8px; border-radius: 6px; color: white; font-weight: bold; font-size: 0.9em;">
                        {job['match_score']}% Match
                    </span>
                </div>
            </div>
            <div style="margin: 10px 0;">
                <span style="background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 4px; font-size: 0.8em; margin-right: 8px;">📍 {job['location']}</span>
                <span style="background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 4px; font-size: 0.8em; margin-right: 8px;">💰 {job['salary']}</span>
                <span style="background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 4px; font-size: 0.8em;">📅 Posted {job['posted_days_ago']}d ago</span>
            </div>
            <p style="font-size: 0.9em; opacity: 0.8;">{job['description'][:150]}...</p>
            <div style="margin-top: 10px;">
                <span style="color: #94a3b8; font-size: 0.85em;">Requirements: {', '.join(job['requirements'][:4])}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            is_applied = job.get('initial_status') == 'Applied'
            if is_applied:
                st.button("Applied ✅", key=f"apply_{job['id']}", disabled=True)
            else:
                if st.button("Apply Now 🔗", key=f"apply_{job['id']}"):
                    job['initial_status'] = 'Applied'
                    # Add to tracker
                    if 'tracked_jobs' not in st.session_state:
                         st.session_state.tracked_jobs = []
                    st.session_state.tracked_jobs.append(job)
                    
                    from utils.notification_service import NotificationService
                    ns = NotificationService()
                    
                    u_email = user_data.get('email')
                    u_phone = user_data.get('phone')
                    
                    if u_email:
                        ns.send_application_email(job, user_email=u_email)
                    if u_phone:
                        ns.send_sms(f"Applied to {job['company']} for {job['title']}.", phone=u_phone)
                    
                    st.toast(f"📧 Email logged to Inbox\n📱 Simulated SMS logged to Dashboard", icon="✅")
                    st.rerun()
        with c2:
            if st.button("Track 📌", key=f"track_{job['id']}"):
                # Add to tracker logic (Mock)
                if 'tracked_jobs' not in st.session_state:
                    st.session_state.tracked_jobs = []
                st.session_state.tracked_jobs.append(job)
                st.toast(f"Tracked {job['title']} at {job['company']}!")
