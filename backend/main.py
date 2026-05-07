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
from skilllens.ml.cv_matcher import extract_cv_skills, rank_jobs_for_cv, skill_gap_summary
from skilllens.ml.model_utils import (
    CATEGORY_MODEL_PATH,
    SALARY_MODEL_PATH,
    model_exists,
)
from skilllens.ml.roadmap_generator import generate_learning_roadmap
from skilllens.ml.train_category_model import predict_category
from skilllens.ml.train_salary_model import predict_salary
from skilllens.skill_extractor import extract_skills

app = FastAPI(
    title="SkillLens AI API",
    description="Backend API for workforce intelligence and career analytics.",
    version="0.2.0",
)


class SkillExtractionRequest(BaseModel):
    text: str


class CVMatchRequest(BaseModel):
    cv_text: str
    top_n: int = 10


class SalaryPredictionRequest(BaseModel):
    category: str
    experience_level: str
    work_type: str
    location: str
    skill_count: int


class CategoryPredictionRequest(BaseModel):
    text: str


class SkillGapRequest(BaseModel):
    cv_text: str
    top_n: int = 10


@app.get("/")
def root():
    return {
        "app": APP_NAME,
        "status": "running",
        "stage": "Stage 2 ML and intelligence layer",
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


@app.post("/cv/extract-skills")
def api_extract_cv_skills(payload: SkillExtractionRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="CV text cannot be empty.")

    return {
        "skills": extract_cv_skills(payload.text),
    }


@app.post("/cv/match-jobs")
def api_match_cv_to_jobs(payload: CVMatchRequest):
    if not payload.cv_text.strip():
        raise HTTPException(status_code=400, detail="CV text cannot be empty.")

    df = load_jobs_from_database()

    if df.empty:
        raise HTTPException(status_code=404, detail="No job data available.")

    ranked = rank_jobs_for_cv(
        cv_text=payload.cv_text,
        jobs_df=df,
        top_n=payload.top_n,
    )

    return ranked.to_dict(orient="records")


@app.post("/cv/skill-gap")
def api_skill_gap(payload: SkillGapRequest):
    if not payload.cv_text.strip():
        raise HTTPException(status_code=400, detail="CV text cannot be empty.")

    df = load_jobs_from_database()

    if df.empty:
        raise HTTPException(status_code=404, detail="No job data available.")

    gap_df = skill_gap_summary(payload.cv_text, df)
    missing_skills = gap_df["skill"].head(payload.top_n).tolist() if not gap_df.empty else []
    roadmap = generate_learning_roadmap(missing_skills)

    return {
        "missing_skills": gap_df.head(payload.top_n).to_dict(orient="records")
        if not gap_df.empty
        else [],
        "roadmap": roadmap,
    }


@app.post("/ml/predict-salary")
def api_predict_salary(payload: SalaryPredictionRequest):
    if not model_exists(SALARY_MODEL_PATH):
        raise HTTPException(
            status_code=404,
            detail="Salary model not found. Run: python -m skilllens.ml.train_salary_model",
        )

    salary = predict_salary(
        category=payload.category,
        experience_level=payload.experience_level,
        work_type=payload.work_type,
        location=payload.location,
        skill_count=payload.skill_count,
    )

    return {
        "predicted_salary_midpoint": salary,
        "estimated_lower_range": round(salary * 0.92, 2),
        "estimated_upper_range": round(salary * 1.08, 2),
    }


@app.post("/ml/predict-category")
def api_predict_category(payload: CategoryPredictionRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    if not model_exists(CATEGORY_MODEL_PATH):
        raise HTTPException(
            status_code=404,
            detail="Category model not found. Run: python -m skilllens.ml.train_category_model",
        )

    category = predict_category(payload.text)

    return {
        "predicted_category": category,
    }