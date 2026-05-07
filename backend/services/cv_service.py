from fastapi import HTTPException

from backend.services.job_service import get_jobs_dataframe
from skilllens.ml.cv_matcher import (
    extract_cv_skills,
    rank_jobs_for_cv,
    skill_gap_summary,
)
from skilllens.ml.roadmap_generator import generate_learning_roadmap
from skilllens.skill_extractor import extract_skills


def extract_skills_from_text(text: str) -> dict:
    """
    Extract skills from general text.
    """
    cleaned = text.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    return {
        "skills": extract_skills(cleaned),
    }


def extract_skills_from_cv(cv_text: str) -> dict:
    """
    Extract technical skills from CV text.
    """
    cleaned = cv_text.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="CV text cannot be empty.")

    return {
        "skills": extract_cv_skills(cleaned),
    }


def match_cv_to_jobs(cv_text: str, top_n: int = 10) -> list[dict]:
    """
    Match CV against job postings.
    """
    cleaned = cv_text.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="CV text cannot be empty.")

    df = get_jobs_dataframe()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No job data available. Run data ingestion first.",
        )

    ranked = rank_jobs_for_cv(
        cv_text=cleaned,
        jobs_df=df,
        top_n=top_n,
    )

    return ranked.to_dict(orient="records")


def analyse_skill_gap(cv_text: str, top_n: int = 10) -> dict:
    """
    Analyse CV skill gaps and generate roadmap.
    """
    cleaned = cv_text.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="CV text cannot be empty.")

    df = get_jobs_dataframe()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No job data available. Run data ingestion first.",
        )

    gap_df = skill_gap_summary(cleaned, df)

    if gap_df.empty:
        missing_skills = []
    else:
        missing_skills = gap_df.head(top_n).to_dict(orient="records")

    missing_skill_names = [
        item["skill"]
        for item in missing_skills
    ]

    roadmap = generate_learning_roadmap(missing_skill_names)

    return {
        "missing_skills": missing_skills,
        "roadmap": roadmap,
    }