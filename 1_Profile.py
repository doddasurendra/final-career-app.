import streamlit as st
import pandas as pd
from utils.data_manager import load_user_data, save_user_data
from utils.resume_parser import extract_text_from_pdf, extract_skills_from_text
from datetime import datetime

# Setup
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

st.title("👤 Your Career Profile")
st.caption("Detailed profiles get 3x more job matches.")

# Load existing data
data = load_user_data() or {}

with st.form("profile_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", value=data.get("name", ""))
        email = st.text_input("Email", value=data.get("email", ""))
        phone = st.text_input("Phone Number", value=data.get("phone", ""))
        location = st.text_input("Current Location", value=data.get("location", ""))

    with col2:
        degree = st.selectbox("Degree", ["B.E / B.Tech", "M.E / M.Tech", "B.Sc", "MCA", "Other"], index=0)
        branch = st.text_input("Branch / Major", value=data.get("branch", "Computer Science Engineering"))
        college = st.text_input("College / University", value=data.get("college", ""))
        grad_year = st.number_input("Graduation Year", min_value=2024, max_value=2030, value=data.get("grad_year", 2026))

    st.markdown("### 🛠️ Skills & Expertise")
    # Pre-fill skills if they exist
    default_skills = data.get("skills", [])
    skills_input = st.text_area("List your Technical Skills (comma separated)", value=", ".join(default_skills))
    
    st.markdown("### 📸 Profile Photo")
    col_pic1, col_pic2 = st.columns([3, 1])
    with col_pic1:
        profile_pic = st.file_uploader("Upload Profile Picture", type=['png', 'jpg', 'jpeg'])
    with col_pic2:
        st.write("") # Spacer
        st.write("")
        remove_pic = st.checkbox("Remove Photo")

    st.markdown("### 📄 Resume Upload")
    uploaded_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)
    
    # Store resumes as a list of dicts
    resumes_data = data.get("resumes", []) # [{'filename': 'x.pdf', 'text': '...', 'skills': [...]}]
    
    if uploaded_files:
        st.info(f"Processing {len(uploaded_files)} new file(s)...")
        
        new_resumes = []
        all_new_skills = set()
        
        for pdf_file in uploaded_files:
             # Check if already exists to avoid dupes (simple check by name)
            if any(r['filename'] == pdf_file.name for r in resumes_data):
                continue

            text = extract_text_from_pdf(pdf_file)
            if text:
                found = extract_skills_from_text(text)
                all_new_skills.update(found)
                
                new_resumes.append({
                    "filename": pdf_file.name,
                    "text": text,
                    "skills": list(found)
                })
        
        if new_resumes:
            resumes_data.extend(new_resumes)
            st.success(f"Added {len(new_resumes)} new resumes! Found skills: {', '.join(all_new_skills)}")
            # Update default skills input if empty
            if not skills_input:
                skills_input = ", ".join(all_new_skills)

    # Display Current Resumes
    if resumes_data:
        st.write("📚 **Stored Resumes:**")
        for i, r in enumerate(resumes_data):
            st.caption(f"{i+1}. {r['filename']} ({len(r['skills'])} skills detected)")
            
    submit = st.form_submit_button("Save Profile")

    if submit:
        # Process Image
        import base64
        pic_data = data.get("profile_pic", None)
        
        if remove_pic:
            pic_data = None
        elif profile_pic:
            pic_data = base64.b64encode(profile_pic.getvalue()).decode("utf-8")

        # Process Skills
        final_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        
        # Calculate Profile Completion
        # Use length of resumes list as factor
        has_resume = len(resumes_data) > 0
        fields = [name, email, phone, college, final_skills, has_resume, pic_data]
        filled_count = sum(1 for f in fields if f)
        completion_score = int((filled_count / len(fields)) * 100)
        
        user_profile = {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "degree": degree,
            "branch": branch,
            "college": college,
            "grad_year": grad_year,
            "skills": final_skills,
            "resumes": resumes_data, # NEW: List of resumes
            "profile_pic": pic_data,
            "profile_completion": completion_score,
            "last_updated": str(datetime.now())
        }
        
        save_user_data(user_profile)
        st.success("✅ Profile Verified & Saved Successfully!")
        st.rerun()

st.markdown("---")
st.subheader("⚙️ Account Settings")

col_acc1, col_acc2 = st.columns(2)

with col_acc1:
    st.info("🤝 **Got a Job? Pass it on!**")
    if st.button("Share App with Friend 📤"):
        share_msg = "Hey! I used this AI Career Assistant to get a job. Check it out!"
        st.code(share_msg, language=None)
        st.toast("Message copied to clipboard! (Simulated)", icon="📋")

    st.markdown("---")
    st.caption("📥 **Backup / Deploy**")
    
    if st.button("📦 Create Project Zip"):
        import zipfile
        import os
        
        # New clean filename to avoid conflicts with the 11GB one
        zip_name = "final_career_app.zip"
        
        # Clear old one if exists
        if os.path.exists(zip_name):
            try: os.remove(zip_name)
            except: pass
            
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("."):
                # Exclude hidden system folders and the zip itself
                if any(part.startswith('.') and part != '.streamlit' for part in root.split(os.sep)):
                    continue
                    
                for file in files:
                    file_path = os.path.join(root, file)
                    # CRITICAL: Do not zip the zip file or temporary data
                    if file.endswith(".zip") or file == "user_data.json":
                        continue
                        
                    zipf.write(file_path, os.path.relpath(file_path, "."))
                    
        st.toast("Optimized ZIP Created!", icon="✅")
        st.rerun()

    import os
    if os.path.exists("final_career_app.zip"):
        with open("final_career_app.zip", "rb") as fp:
            st.download_button(
                label="⬇️ Download Source Code",
                data=fp,
                file_name="ai_career_assistant_source.zip",
                mime="application/zip"
            )

with col_acc2:
    st.error("🚨 **Danger Zone**")
    if st.button("🗑️ Delete Account & Reset App"):
        import os
        if os.path.exists("user_data.json"):
            os.remove("user_data.json")
        st.session_state.clear()
        st.success("Account deleted successfully! Refreshing...")
        import time
        time.sleep(1)
        st.rerun()
