import pandas as pd
import streamlit as st

from utils.data_manager import load_resume_data
from faiss_index.index_builder import build_faiss_index
from search.search_engine import search_resumes

import re

def get_candidate_name(filename):
    # Remove extension
    name = filename.rsplit(".", 1)[0]

    # Remove "_Validated"
    name = name.replace("_Validated", "")

    # Remove duplicate marker like (002)
    name = re.sub(r"\(\d+\)", "", name)

    # Insert spaces before capital letters
    name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)

    # Remove extra spaces
    name = " ".join(name.split())

    return name

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------
# Load Resources (Runs only once)
# ---------------------------------------------------

@st.cache_resource
def load_resources():
    resume_data = load_resume_data()
    index = build_faiss_index(resume_data)
    return resume_data, index


resume_data, index = load_resources()


# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("📄 AI Resume Screener")

st.markdown("""
Find the most relevant candidates using **Semantic Search**, **Sentence Transformers**, and **FAISS**.
""")

st.divider()


# ---------------------------------------------------
# Search Box
# ---------------------------------------------------

query = st.text_area(
    "📝 Enter Job Description",
    height=180,
    placeholder="""
Example:

Looking for a Python Developer with experience in:

• Python
• Machine Learning
• SQL
• Flask
• REST APIs
• Data Analysis
"""
)

min_score = st.slider(
    "🎯 Minimum Match Score",
    min_value=0,
    max_value=100,
    value=0,
    step=5
)

search = st.button(
    "🔍 Search Candidates",
    use_container_width=True
)


# ---------------------------------------------------
# Search
# ---------------------------------------------------

if search:

    if not query.strip():
        st.warning("Please enter a job description.")
        st.stop()

    results = search_resumes(
        query=query,
        index=index,
        resume_data=resume_data,
        top_k=10
    )

    results = [
        resume
        for resume in results
        if resume["overall_score"] * 100 >= min_score
    ]

    results = results[:5]

    if results:
        st.success(f"Found {len(results)} matching candidates.")
    else:
        st.warning("No candidates matched the selected criteria.")

    if results:

        export_data = []

        for resume in results:
            export_data.append({
                "Candidate": get_candidate_name(resume["filename"]),
                "Email": resume["email"] or "Not Available",
                "Overall Match": round(resume["overall_score"] * 100, 1),
                "Semantic Match": round(resume["semantic_score"] * 100, 1),
                "Skill Match": round(resume["skill_score"] * 100, 1),
                "Matching Skills": ", ".join(resume["matched_skills"]),
                "Missing Skills": ", ".join([
                    skill
                    for skill in resume["required_skills"]
                    if skill not in resume["matched_skills"]
                ])
            })

        export_df = pd.DataFrame(export_data)

        csv = export_df.to_csv(index=False)

        st.download_button(
            label="📊 Download Candidate Results",
            data=csv,
            file_name="resume_screening_results.csv",
            mime="text/csv"
        )    

    st.write("## 🏆 Top Candidates")

    for rank, resume in enumerate(results, start=1):

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            # -----------------------------
            # Left Column
            # -----------------------------

            with col1:

                candidate_name = get_candidate_name(resume["filename"])

                st.subheader(f"🏆 {candidate_name}")

                # st.write(f"**📄 Resume :** {candidate_name}")
                #SKILLS
                if resume["skills"]:

                    st.write("**🏷 Skills**")

                    skills = resume["skills"]

                    for i in range(0, len(skills), 4):

                        cols = st.columns(4)

                        for j in range(4):

                            if i + j < len(skills):
                                cols[j].success(skills[i + j])

                email = resume["email"] if resume["email"] else "Not Available"                

                st.write(f"**📧 Email:** {email}")

            # -----------------------------
            # Right Column
            # -----------------------------

            with col2:

                st.metric(
                    label="🎯 Overall Match",
                    value=f"{resume['overall_score'] * 100:.1f}%"
                )

                st.caption("Based on semantic similarity + required skill match")

            # -----------------------------
            # Progress Bar
            # -----------------------------

            st.progress(float(resume["overall_score"]))

            score_col1, score_col2 = st.columns(2)

            with score_col1:
               st.write(
                   f"🧠 **Semantic Match:** "
                   f"{resume['semantic_score'] * 100:.1f}%"
                )

            with score_col2:
               st.write(
                   f"🏷 **Skill Match:** "
                   f"{resume['skill_score'] * 100:.1f}%"
                ) 

            # -----------------------------
            # Skill Analysis
            # -----------------------------

            if resume["matched_skills"]:

                st.write("**✅ Matching Skills**")

                for skill in resume["matched_skills"]:
                    st.success(skill)


            missing_skills = [
                skill
                for skill in resume["required_skills"]
                if skill not in resume["matched_skills"]
            ]

            if missing_skills:

                st.write("**❌ Missing Skills**")

                for skill in missing_skills:
                    st.error(skill)    

            # -----------------------------
            # Resume Preview
            # -----------------------------

            with st.expander("📖 Resume Preview"):

                preview = resume["text"][:700]

                if len(resume["text"]) > 700:
                    preview += "..."

                st.write(preview)

            # -----------------------------
            # Download Resume
            # -----------------------------

            try:

                with open(resume["filepath"], "rb") as file:

                    st.download_button(
                        label="📥 Download Resume",
                        data=file,
                        file_name=resume["filename"],
                        use_container_width=True
                    )

            except FileNotFoundError:

                st.error("Resume file not found.")

            st.write("")
