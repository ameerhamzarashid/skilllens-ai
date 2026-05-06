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
            background:
                radial-gradient(circle at top left, rgba(124, 58, 237, 0.08), transparent 30%),
                radial-gradient(circle at bottom right, rgba(34, 197, 94, 0.10), transparent 28%),
                linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 55%, #F0FDF4 100%);
            color: #111827;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #E5E7EB;
            box-shadow: 8px 0 25px rgba(17, 24, 39, 0.04);
        }

        [data-testid="stSidebar"] * {
            color: #111827 !important;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #6D28D9 !important;
            font-weight: 900 !important;
        }

        [data-testid="stSidebar"] label {
            color: #374151 !important;
            font-weight: 700 !important;
        }

        .main-title {
            font-size: 3rem;
            font-weight: 950;
            letter-spacing: -1.2px;
            color: #111827;
            margin-bottom: 0rem;
        }

        .main-title::after {
            content: "";
            display: block;
            width: 140px;
            height: 5px;
            background: linear-gradient(90deg, #6D28D9, #22C55E);
            margin-top: 0.55rem;
            border-radius: 999px;
        }

        .subtitle {
            color: #4B5563;
            font-size: 1.08rem;
            margin-top: 0.8rem;
            margin-bottom: 1.5rem;
        }

        .metric-card {
            padding: 1.25rem;
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid #E5E7EB;
            box-shadow:
                0 18px 45px rgba(17, 24, 39, 0.08),
                inset 0 0 0 1px rgba(255, 255, 255, 0.8);
            margin-bottom: 1rem;
        }

        .metric-card:hover {
            border-color: rgba(109, 40, 217, 0.35);
            box-shadow:
                0 20px 50px rgba(109, 40, 217, 0.12),
                0 10px 35px rgba(34, 197, 94, 0.08);
            transition: 0.25s ease;
        }

        .big-number {
            font-size: 2.25rem;
            font-weight: 950;
            color: #6D28D9;
            line-height: 1;
        }

        .metric-label {
            color: #6B7280;
            font-size: 0.9rem;
            margin-top: 0.45rem;
            text-transform: uppercase;
            letter-spacing: 0.45px;
            font-weight: 700;
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

        .insight-box h3 {
            color: #6D28D9;
            font-weight: 900;
            margin-bottom: 0.5rem;
        }

        .insight-box p {
            color: #374151;
            font-size: 1rem;
            line-height: 1.55;
        }

        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 12px 35px rgba(17, 24, 39, 0.06);
        }

        [data-testid="stMetricLabel"] {
            color: #6B7280 !important;
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: #6D28D9 !important;
            font-weight: 950;
        }

        .stButton > button {
            background: linear-gradient(90deg, #6D28D9, #22C55E) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 14px !important;
            font-weight: 800 !important;
            padding: 0.55rem 1rem !important;
            box-shadow: 0 10px 25px rgba(109, 40, 217, 0.18);
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #5B21B6, #16A34A) !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
            transition: 0.2s ease;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.4rem;
            border-bottom: 1px solid #E5E7EB;
        }

        .stTabs [data-baseweb="tab"] {
            background: #FFFFFF;
            color: #374151;
            border-radius: 14px 14px 0 0;
            border: 1px solid #E5E7EB;
            padding: 0.65rem 1rem;
            font-weight: 800;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #6D28D9, #22C55E) !important;
            color: #FFFFFF !important;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 12px 35px rgba(17, 24, 39, 0.05);
        }

        .stTextInput input {
            background: #FFFFFF !important;
            color: #111827 !important;
            border: 1px solid #D1D5DB !important;
            border-radius: 12px !important;
        }

        .stSelectbox div {
            color: #111827 !important;
        }

        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #6D28D9, #22C55E, transparent);
            margin: 1.5rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_chart_style(fig):
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#111827"),
        margin=dict(l=20, r=20, t=55, b=20),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            font=dict(color="#111827"),
        ),
        colorway=[
            "#6D28D9",
            "#22C55E",
            "#A78BFA",
            "#86EFAC",
            "#4C1D95",
            "#15803D",
        ],
    )

    fig.update_xaxes(
        gridcolor="#E5E7EB",
        zerolinecolor="#E5E7EB",
        linecolor="#D1D5DB",
        color="#374151",
    )

    fig.update_yaxes(
        gridcolor="#E5E7EB",
        zerolinecolor="#E5E7EB",
        linecolor="#D1D5DB",
        color="#374151",
    )

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
            color_discrete_sequence=["#6D28D9"],
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
            color_discrete_sequence=[
                "#6D28D9",
                "#22C55E",
                "#A78BFA",
            ],
        )

        st.plotly_chart(apply_chart_style(fig), use_container_width=True)

    location_df = jobs_by_location(filtered)

    fig = px.bar(
        location_df,
        x="location",
        y="count",
        title="Job Demand by Location",
        labels={"location": "Location", "count": "Job Count"},
        color_discrete_sequence=["#22C55E"],
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
        color="count",
        color_continuous_scale=[
            [0, "#DCFCE7"],
            [0.5, "#A78BFA"],
            [1, "#6D28D9"],
        ],
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
        color="avg_salary",
        color_continuous_scale=[
            [0, "#DCFCE7"],
            [0.5, "#86EFAC"],
            [1, "#6D28D9"],
        ],
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