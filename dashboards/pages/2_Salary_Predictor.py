import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from skilllens.analytics import load_jobs_from_database
from skilllens.config import JOB_CATEGORIES, SAMPLE_JOBS_PATH
from skilllens.ml.model_utils import (
    SALARY_MODEL_PATH,
    SALARY_REPORT_PATH,
    load_json_report,
    model_exists,
)
from skilllens.ml.train_salary_model import predict_salary, train_salary_model


st.set_page_config(
    page_title="Salary Predictor",
    page_icon="💷",
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
        .result-box {
            padding: 1.5rem;
            border-radius: 24px;
            background:
                linear-gradient(135deg, rgba(109, 40, 217, 0.08), rgba(34, 197, 94, 0.10)),
                #FFFFFF;
            border: 1px solid rgba(109, 40, 217, 0.18);
            box-shadow: 0 18px 45px rgba(17, 24, 39, 0.07);
            margin-top: 1rem;
            margin-bottom: 1.2rem;
        }
        .salary-number {
            font-size: 3rem;
            color: #6D28D9;
            font-weight: 950;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.markdown(
    """
    <div class="main-title">Salary Predictor</div>
    <div class="subtitle">
    Predict estimated salary midpoint from role, experience, location and skill count.
    </div>
    """,
    unsafe_allow_html=True,
)

if not model_exists(SALARY_MODEL_PATH):
    st.warning("Salary model has not been trained yet.")

    if st.button("Train Salary Model Now"):
        with st.spinner("Training salary model..."):
            report = train_salary_model()
        st.success("Salary model trained successfully.")
        st.json(report)

    st.stop()

report = load_json_report(SALARY_REPORT_PATH)

with st.expander("Model Report"):
    st.json(report)

jobs_df = load_jobs_from_database()

locations = ["London", "Newcastle", "Manchester", "Edinburgh", "Glasgow", "Birmingham", "Leeds", "Bristol", "Remote UK"]

if not jobs_df.empty and "location" in jobs_df.columns:
    locations = sorted(jobs_df["location"].dropna().unique().tolist())

experience_levels = [
    "Entry Level",
    "Junior",
    "Mid Level",
    "Senior",
]

work_types = [
    "Remote",
    "Hybrid",
    "Onsite",
]

col1, col2 = st.columns(2)

with col1:
    category = st.selectbox("Role Category", JOB_CATEGORIES)
    experience_level = st.selectbox("Experience Level", experience_levels)

with col2:
    location = st.selectbox("Location", locations)
    work_type = st.selectbox("Work Type", work_types)

skill_count = st.slider(
    "Number of relevant skills",
    min_value=1,
    max_value=20,
    value=8,
)

if st.button("Predict Salary"):
    salary = predict_salary(
        category=category,
        experience_level=experience_level,
        work_type=work_type,
        location=location,
        skill_count=skill_count,
    )

    lower = salary * 0.92
    upper = salary * 1.08

    st.markdown(
        f"""
        <div class="result-box">
            <h3>Predicted Salary Range</h3>
            <div class="salary-number">£{lower:,.0f} - £{upper:,.0f}</div>
            <p>Estimated midpoint: £{salary:,.0f}</p>
            <p>This is a Stage 2 model trained on the generated SkillLens job dataset.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("Choose inputs and click Predict Salary.")