import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import plotly.express as px
import streamlit as st

from skilllens.analytics import load_jobs_from_database
from skilllens.config import SAMPLE_JOBS_PATH
from skilllens.ml.cv_matcher import extract_cv_skills, rank_jobs_for_cv
from skilllens.skill_extractor import extract_skills


st.set_page_config(
    page_title="CV Job Matcher",
    page_icon="🎯",
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
        .insight-box {
            padding: 1.35rem;
            border-radius: 24px;
            background:
                linear-gradient(135deg, rgba(109, 40, 217, 0.08), rgba(34, 197, 94, 0.10)),
                #FFFFFF;
            border: 1px solid rgba(109, 40, 217, 0.18);
            box-shadow: 0 18px 45px rgba(17, 24, 39, 0.07);
            margin-top: 1rem;
            margin-bottom: 1.2rem;
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
    <div class="main-title">CV Job Matcher</div>
    <div class="subtitle">
    Paste your CV text and rank job postings by skill match score.
    </div>
    """,
    unsafe_allow_html=True,
)

jobs_df = load_jobs()

if jobs_df.empty:
    st.error("No job data found. Run data generation and ingestion first.")
    st.stop()

example_cv = """
Data Scientist with experience in Python, SQL, Pandas, NumPy, scikit-learn,
machine learning, Power BI, Tableau, FastAPI, Docker, PostgreSQL and forecasting.
Built dashboards, predictive models and data pipelines for business insight.
"""

cv_text = st.text_area(
    "Paste CV text",
    value=example_cv,
    height=220,
)

top_n = st.sidebar.slider(
    "Number of job matches",
    min_value=5,
    max_value=50,
    value=15,
)

category_filter = st.sidebar.multiselect(
    "Filter by category",
    sorted(jobs_df["category"].dropna().unique().tolist()),
    default=sorted(jobs_df["category"].dropna().unique().tolist()),
)

filtered_jobs = jobs_df[jobs_df["category"].isin(category_filter)].copy()

if st.button("Analyse CV Match"):
    cv_skills = extract_cv_skills(cv_text)

    st.markdown(
        f"""
        <div class="insight-box">
            <h3>Extracted CV Skills</h3>
            <p>{", ".join(cv_skills) if cv_skills else "No known technical skills detected."}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ranked = rank_jobs_for_cv(cv_text, filtered_jobs, top_n=top_n)

    if ranked.empty:
        st.warning("No matching jobs found.")
        st.stop()

    col1, col2, col3 = st.columns(3)

    col1.metric("Best Match", f"{ranked.iloc[0]['match_score']}%")
    col2.metric("Matched Skills", int(ranked.iloc[0]["matched_skill_count"]))
    col3.metric("Required Skills", int(ranked.iloc[0]["required_skill_count"]))

    fig = px.bar(
        ranked.head(10),
        x="match_score",
        y="title",
        color="match_score",
        orientation="h",
        title="Top CV-to-Job Match Scores",
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

    display_cols = [
        "match_score",
        "title",
        "company",
        "location",
        "category",
        "matched_skills_text",
        "missing_skills_text",
    ]

    st.dataframe(
        ranked[display_cols],
        use_container_width=True,
    )
else:
    st.info("Paste your CV text and click Analyse CV Match.")