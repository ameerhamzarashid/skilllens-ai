import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import plotly.express as px
import streamlit as st

from skilllens.analytics import load_jobs_from_database
from skilllens.config import SAMPLE_JOBS_PATH
from skilllens.ml.cv_matcher import extract_cv_skills, skill_gap_summary
from skilllens.ml.roadmap_generator import generate_learning_roadmap, roadmap_to_markdown
from skilllens.skill_extractor import extract_skills


st.set_page_config(
    page_title="Skill Gap Analysis",
    page_icon="🧭",
    layout="wide",
)


def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(124, 58, 237, 0.08), transparent 30%),
                radial-gradient(circle at bottom right, rgba(34, 197, 94, 0.10), transparent 28%),
                linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 55%, #F0FDF4 100%);
            color: #111827;
        }
        .main-title {
            font-size: 2.8rem;
            font-weight: 950;
            color: #111827;
            margin-bottom: 0rem;
        }
        .main-title::after {
            content: "";
            display: block;
            width: 130px;
            height: 5px;
            background: linear-gradient(90deg, #6D28D9, #22C55E);
            margin-top: 0.55rem;
            border-radius: 999px;
        }
        .subtitle {
            color: #4B5563;
            font-size: 1.05rem;
            margin-top: 0.8rem;
            margin-bottom: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_jobs():
    df = load_jobs_from_database()

    if not df.empty:
        return df

    if SAMPLE_JOBS_PATH.exists():
        import pandas as pd

        fallback = pd.read_csv(SAMPLE_JOBS_PATH)

        if "extracted_skills" not in fallback.columns:
            fallback["extracted_skills"] = fallback["description"].apply(
                lambda text: ", ".join(extract_skills(text))
            )

        return fallback

    return df


inject_css()

st.markdown(
    """
    <div class="main-title">Skill Gap Analysis</div>
    <div class="subtitle">
    Compare your CV skills against market demand and generate a personalised learning roadmap.
    </div>
    """,
    unsafe_allow_html=True,
)

jobs_df = load_jobs()

if jobs_df.empty:
    st.error("No job data found. Run data generation and ingestion first.")
    st.stop()

example_cv = """
Data Analyst and Data Scientist with Python, SQL, Excel, Power BI,
Pandas, NumPy, machine learning, Tableau and PostgreSQL experience.
"""

cv_text = st.text_area(
    "Paste CV text",
    value=example_cv,
    height=220,
)

target_categories = st.sidebar.multiselect(
    "Target Role Categories",
    sorted(jobs_df["category"].dropna().unique().tolist()),
    default=["Data Scientist", "Data Engineer", "AI Engineer"]
    if set(["Data Scientist", "Data Engineer", "AI Engineer"]).issubset(set(jobs_df["category"].unique()))
    else sorted(jobs_df["category"].dropna().unique().tolist()),
)

filtered_jobs = jobs_df[jobs_df["category"].isin(target_categories)].copy()

if st.button("Analyse Skill Gap"):
    cv_skills = extract_cv_skills(cv_text)
    gap_df = skill_gap_summary(cv_text, filtered_jobs)

    col1, col2, col3 = st.columns(3)

    col1.metric("CV Skills Found", len(cv_skills))
    col2.metric("Target Jobs", len(filtered_jobs))
    col3.metric("Missing Skill Types", len(gap_df))

    st.subheader("Your Extracted Skills")
    st.write(", ".join(cv_skills) if cv_skills else "No known skills detected.")

    st.subheader("Most Common Missing Skills")

    if gap_df.empty:
        st.success("No major missing skills found.")
    else:
        fig = px.bar(
            gap_df.head(15),
            x="missing_count",
            y="skill",
            orientation="h",
            color="missing_count",
            title="Most Common Missing Skills Across Target Jobs",
            color_continuous_scale=[
                [0, "#DCFCE7"],
                [0.5, "#A78BFA"],
                [1, "#6D28D9"],
            ],
        )

        fig.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#111827"),
            yaxis=dict(categoryorder="total ascending"),
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(gap_df, use_container_width=True)

        missing_skills = gap_df["skill"].head(8).tolist()
        roadmap = generate_learning_roadmap(missing_skills)

        st.subheader("Personalised Learning Roadmap")
        st.markdown(roadmap_to_markdown(roadmap))
else:
    st.info("Paste your CV and click Analyse Skill Gap.")