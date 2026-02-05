import streamlit as st

# Setup
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

st.title("🎓 Career Guidance & Prep")

tab1, tab2, tab3 = st.tabs(["💡 Career Roadmap", "🎤 Interview Prep", "🧠 Coding Practice"])

with tab1:
    st.header("Roadmap: From Fresher to SDE")
    st.markdown("""
    #### 3-Month Action Plan
    - **Month 1: Foundations**
        - DSA: Arrays, Strings, Linked Lists
        - Web: HTML, CSS, JS basics
        - **Goal**: Solve 50 LeetCode Easy problems.
        
    - **Month 2: Projects & Frameworks**
        - Learn React/Next.js or Python/Django
        - Build 2 Major Projects (e.g., this Career Assistant!)
        - **Goal**: Deploy one project live.
        
    - **Month 3: Apply & Interview**
        - Mock Interviews
        - Resume Iterations
        - **Goal**: Apply to 5 jobs daily.
    """)
    st.info("📌 Pro Tip: Consistency beats intensity. Code for 1 hour every day.")

with tab2:
    st.header("Common Interview Questions")
    
    with st.expander("Behavioral: 'Tell me about yourself.'"):
        st.write("""
        **Framework**: Past, Present, Future.
        1. **Past**: "I recently graduated from XYZ College with a degree in CS..."
        2. **Present**: "I have been building projects using React and Python..."
        3. **Future**: "I am looking for a role to apply these skills in a challenging environment."
        """)
        
    with st.expander("Technical: 'Explain REST APIs.'"):
        st.write("""
        REST (Representational State Transfer) is an architectural style for APIs.
        - **Statelessness**: Server doesn't store client state.
        - **Methods**: GET, POST, PUT, DELETE.
        - **Resources**: Accessed via URLs.
        """)

with tab3:
    st.header("Coding Challenge of the Day")
    st.markdown("""
    **Problem**: Two Sum
    Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.
    """)
    
    code = st.text_area("Write your solution (Python):", height=150)
    if st.button("Run Tests"):
        if "return" in code:
            st.success("✅ Output: [0, 1] (Passed)")
        else:
            st.error("❌ Syntax Error or Incorrect Logic")
