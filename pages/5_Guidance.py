import streamlit as st

# Setup
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

st.title("🎓 Career Guidance")
st.markdown("""
### 💡 Roadmaps
- **Month 1**: Solve 50 LeetCode Easy problems.
- **Month 2**: Build 2 major projects.
- **Month 3**: Start applying!
""")
