from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from skilllens.analytics import (
    get_summary_metrics,
    jobs_by_category,
    load_jobs_from_database,
    salary_by_category,
    top_skills,
)
from skilllens.config import APP_NAME
from skilllens.skill_extractor import extract_skills

app = FastAPI(
    title="SkillLens AI API",
    description="Stage 1 backend API for workforce intelligence and career analytics.",
    version="0.1.0",
)


class SkillExtractionRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "app": APP_NAME,
        "status": "running",
        "stage": "Stage 1 foundation",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.get("/summary")
def summary():
    df = load_jobs_from_database()

    if df.empty:
        return {
            "message": "No job data found. Run ingestion first.",
            "summary": {},
        }

    return get_summary_metrics(df)


@app.get("/jobs")
def jobs(limit: int = 20):
    df = load_jobs_from_database()

    if df.empty:
        return []

    return df.head(limit).to_dict(orient="records")


@app.get("/skills/top")
def skills_top(limit: int = 20):
    df = load_jobs_from_database()

    if df.empty:
        return []

    return top_skills(df, top_n=limit).to_dict(orient="records")


@app.get("/analytics/categories")
def analytics_categories():
    df = load_jobs_from_database()

    if df.empty:
        return []

    return jobs_by_category(df).to_dict(orient="records")


@app.get("/analytics/salary-by-category")
def analytics_salary_by_category():
    df = load_jobs_from_database()

    if df.empty:
        return []

    return salary_by_category(df).round(2).to_dict(orient="records")


@app.post("/extract-skills")
def api_extract_skills(payload: SkillExtractionRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    return {
        "skills": extract_skills(payload.text),
    }