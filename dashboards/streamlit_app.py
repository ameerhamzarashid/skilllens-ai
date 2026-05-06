import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import plotly.express as px
import streamlit as st

from skilllens.analytics import (
    get_summary_metrics,
    jobs_by_category,
    jobs_by_location,
    load_jobs_from_database,
    salary_by_category,
    top_skills,
    work_type_distribution,
)
from skilllens.config import APP_NAME, SAMPLE_JOBS_PATH
from skilllens.skill_extractor import extract_skills


st.set_page_config(
    page_title="SkillLens AI",
    page_icon="🔎",
    layout="wide",
)


def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #07111F 0%, #0B1220 50%, #111827 100%);
            color: #F9FAFB;
        }

        [data-testid="stSidebar"] {
            background-color: #0B1220;
            border-right: 1px solid #1F2937;
        }

        .main-title {
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: -1px;
            color: #F9FAFB;
            margin-bottom: 0rem;
        }

        .subtitle {
            color: #9CA3AF;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }

        .metric-card {
            padding: 1.2rem;
            border-radius: 18px;
            background: rgba(17, 24, 39, 0.92);
            border: 1px solid #1F2937;
            box-shadow: 0 16px 40px rgba(0,0,0,0.35);
            margin-bottom: 1rem;
        }

        .big-number {
            font-size: 2.2rem;
            font-weight: 900;
            color: #38BDF8;
            line-height: 1;
        }

        .metric-label {
            color: #9CA3AF;
            font-size: 0.9rem;
            margin-top: 0.4rem;
        }

        .insight-box {
            padding: 1.2rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(34,197,94,0.08));
            border: 1px solid rgba(56,189,248,0.35);
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_chart_style(fig):
    fig.update_layout(
        paper_bgcolor="#07111F",
        plot_bgcolor="#111827",
        font=dict(color="#F9FAFB"),
        margin=dict(l=20, r=20, t=55, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )

    fig.update_xaxes(gridcolor="#1F2937")
    fig.update_yaxes(gridcolor="#1F2937")

    return fig


@st.cache_data(show_spinner=False)
def load_data():
    """
    Load from database first.
    If database is empty, load raw CSV if available.
    """
    df = load_jobs_from_database()

    if not df.empty:
        return df, "database"

    if SAMPLE_JOBS_PATH.exists():
        fallback = pd.read_csv(SAMPLE_JOBS_PATH)

        if "extracted_skills" not in fallback.columns:
            fallback["extracted_skills"] = fallback["description"].apply(
                lambda text: ", ".join(extract_skills(text))
            )

        return fallback, "sample_csv"

    return pd.DataFrame(), "none"


inject_css()

st.markdown(
    """
    <div class="main-title">SkillLens AI</div>
    <div class="subtitle">
    Workforce Intelligence and Career Analytics Platform
    </div>
    """,
    unsafe_allow_html=True,
)

df, source = load_data()

if df.empty:
    st.error(
        "No data found. Run these commands first: "
        "`python -m data_platform.generate_sample_jobs` and "
        "`python -m data_platform.ingest_jobs`."
    )
    st.stop()

st.sidebar.title("SkillLens AI")
st.sidebar.caption(f"Data source: {source}")

categories = sorted(df["category"].dropna().unique().tolist())
locations = sorted(df["location"].dropna().unique().tolist())
work_types = sorted(df["work_type"].dropna().unique().tolist())

selected_categories = st.sidebar.multiselect(
    "Role Categories",
    categories,
    default=categories,
)

selected_locations = st.sidebar.multiselect(
    "Locations",
    locations,
    default=locations,
)

selected_work_types = st.sidebar.multiselect(
    "Work Type",
    work_types,
    default=work_types,
)

filtered = df[
    df["category"].isin(selected_categories)
    & df["location"].isin(selected_locations)
    & df["work_type"].isin(selected_work_types)
].copy()

summary = get_summary_metrics(filtered)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="big-number">{summary['total_jobs']}</div>
            <div class="metric-label">Jobs Analysed</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="big-number">{summary['companies']}</div>
            <div class="metric-label">Companies</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="big-number">{summary['locations']}</div>
            <div class="metric-label">Locations</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="big-number">£{summary['avg_salary']:,.0f}</div>
            <div class="metric-label">Average Salary</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="big-number">{summary['skills']}</div>
            <div class="metric-label">Unique Skills</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="insight-box">
        <h3>Stage 1 Platform Status</h3>
        <p>
        This dashboard is powered by the SkillLens AI data platform foundation.
        It includes job data generation, skill extraction, database ingestion,
        analytics functions and early workforce intelligence visuals.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Market Overview",
        "Skill Trends",
        "Salary Intelligence",
        "Job Explorer",
    ]
)

with tab1:
    left, right = st.columns(2)

    with left:
        category_df = jobs_by_category(filtered)

        fig = px.bar(
            category_df,
            x="category",
            y="count",
            title="Job Demand by Role Category",
            labels={"category": "Role Category", "count": "Job Count"},
        )

        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_chart_style(fig), use_container_width=True)

    with right:
        work_df = work_type_distribution(filtered)

        fig = px.pie(
            work_df,
            names="work_type",
            values="count",
            title="Remote vs Hybrid vs Onsite",
        )

        st.plotly_chart(apply_chart_style(fig), use_container_width=True)

    location_df = jobs_by_location(filtered)

    fig = px.bar(
        location_df,
        x="location",
        y="count",
        title="Job Demand by Location",
        labels={"location": "Location", "count": "Job Count"},
    )

    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(apply_chart_style(fig), use_container_width=True)

with tab2:
    skills_df = top_skills(filtered, top_n=25)

    fig = px.bar(
        skills_df,
        x="count",
        y="skill",
        orientation="h",
        title="Top In-Demand Skills",
        labels={"count": "Demand Count", "skill": "Skill"},
    )

    fig.update_layout(yaxis=dict(categoryorder="total ascending"))

    st.plotly_chart(apply_chart_style(fig), use_container_width=True)

    st.dataframe(skills_df, use_container_width=True)

with tab3:
    salary_df = salary_by_category(filtered)

    fig = px.bar(
        salary_df,
        x="category",
        y="avg_salary",
        title="Average Salary by Role Category",
        labels={"category": "Role Category", "avg_salary": "Average Salary GBP"},
    )

    fig.update_layout(xaxis_tickangle=-35)

    st.plotly_chart(apply_chart_style(fig), use_container_width=True)

    st.dataframe(salary_df.round(2), use_container_width=True)

with tab4:
    st.subheader("Search Job Postings")

    search_text = st.text_input(
        "Search title, company, location, skill or description",
        "",
    )

    explorer = filtered.copy()

    if search_text:
        query = search_text.lower()

        explorer = explorer[
            explorer["title"].str.lower().str.contains(query, na=False)
            | explorer["company"].str.lower().str.contains(query, na=False)
            | explorer["location"].str.lower().str.contains(query, na=False)
            | explorer["description"].str.lower().str.contains(query, na=False)
            | explorer["extracted_skills"].str.lower().str.contains(query, na=False)
        ]

    display_columns = [
        "title",
        "company",
        "location",
        "category",
        "experience_level",
        "work_type",
        "salary_min",
        "salary_max",
        "extracted_skills",
    ]

    available_columns = [col for col in display_columns if col in explorer.columns]

    st.dataframe(
        explorer[available_columns].head(100),
        use_container_width=True,
    )