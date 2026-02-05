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
    default_skills = data.get("skills", [])
    skills_input = st.text_area("List your Technical Skills (comma separated)", value=", ".join(default_skills))
    
    st.markdown("### 📸 Profile Photo")
    profile_pic = st.file_uploader("Upload Profile Picture", type=['png', 'jpg', 'jpeg'])
    remove_pic = st.checkbox("Remove Photo")

    st.markdown("### 📄 Resume Upload")
    uploaded_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)
    
    resumes_data = data.get("resumes", [])
    
    if uploaded_files:
        new_resumes = []
        for pdf_file in uploaded_files:
            if any(r['filename'] == pdf_file.name for r in resumes_data): continue
            text = extract_text_from_pdf(pdf_file)
            if text:
                found = extract_skills_from_text(text)
                new_resumes.append({"filename": pdf_file.name, "text": text, "skills": list(found)})
        if new_resumes:
            resumes_data.extend(new_resumes)
            st.success(f"Added {len(new_resumes)} resumes!")

    submit = st.form_submit_button("Save Profile")

    if submit:
        import base64
        final_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        user_profile = {
            "name": name, "email": email, "phone": phone, "location": location,
            "degree": degree, "branch": branch, "college": college, "grad_year": grad_year,
            "skills": final_skills, "resumes": resumes_data,
            "profile_completion": 80, "last_updated": str(datetime.now())
        }
        save_user_data(user_profile)
        st.success("✅ Profile Saved!")
        st.rerun()

st.markdown("---")
st.subheader("⚙️ Account Settings")
if st.button("🗑️ Delete Account"):
    import os
    if os.path.exists("user_data.json"): os.remove("user_data.json")
    st.session_state.clear()
    st.rerun()
