import pandas as pd
from sqlalchemy import text

from skilllens.database import engine
from skilllens.skill_extractor import string_to_skills


def load_jobs_from_database() -> pd.DataFrame:
    """
    Load all job postings from database.
    """
    query = "SELECT * FROM job_postings"

    try:
        return pd.read_sql(query, engine)
    except Exception:
        return pd.DataFrame()


def get_summary_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate headline metrics.
    """
    if df.empty:
        return {
            "total_jobs": 0,
            "companies": 0,
            "locations": 0,
            "avg_salary": 0,
            "skills": 0,
        }

    all_skills = []

    if "extracted_skills" in df.columns:
        for skill_text in df["extracted_skills"].dropna():
            all_skills.extend(string_to_skills(skill_text))

    salary_mid = None

    if "salary_min" in df.columns and "salary_max" in df.columns:
        salary_mid = ((df["salary_min"] + df["salary_max"]) / 2).mean()

    return {
        "total_jobs": int(len(df)),
        "companies": int(df["company"].nunique()) if "company" in df.columns else 0,
        "locations": int(df["location"].nunique()) if "location" in df.columns else 0,
        "avg_salary": round(float(salary_mid), 2) if pd.notna(salary_mid) else 0,
        "skills": int(len(set(all_skills))),
    }


def top_skills(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Return top extracted skills.
    """
    if df.empty or "extracted_skills" not in df.columns:
        return pd.DataFrame(columns=["skill", "count"])

    rows = []

    for _, row in df.iterrows():
        skills = string_to_skills(row["extracted_skills"])

        for skill in skills:
            rows.append({"skill": skill})

    if not rows:
        return pd.DataFrame(columns=["skill", "count"])

    out = (
        pd.DataFrame(rows)
        .value_counts("skill")
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(top_n)
    )

    return out


def jobs_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count jobs by role category.
    """
    if df.empty or "category" not in df.columns:
        return pd.DataFrame(columns=["category", "count"])

    return (
        df.groupby("category", as_index=False)
        .size()
        .rename(columns={"size": "count"})
        .sort_values("count", ascending=False)
    )


def salary_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Average salary by category.
    """
    if df.empty:
        return pd.DataFrame(columns=["category", "avg_salary"])

    temp = df.copy()
    temp["salary_mid"] = (temp["salary_min"] + temp["salary_max"]) / 2

    return (
        temp.groupby("category", as_index=False)
        .agg(avg_salary=("salary_mid", "mean"))
        .sort_values("avg_salary", ascending=False)
    )


def jobs_by_location(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count jobs by location.
    """
    if df.empty or "location" not in df.columns:
        return pd.DataFrame(columns=["location", "count"])

    return (
        df.groupby("location", as_index=False)
        .size()
        .rename(columns={"size": "count"})
        .sort_values("count", ascending=False)
    )


def work_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count remote/hybrid/onsite jobs.
    """
    if df.empty or "work_type" not in df.columns:
        return pd.DataFrame(columns=["work_type", "count"])

    return (
        df.groupby("work_type", as_index=False)
        .size()
        .rename(columns={"size": "count"})
        .sort_values("count", ascending=False)
    )


def run_basic_sql_healthcheck() -> bool:
    """
    Check if database connection works.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False