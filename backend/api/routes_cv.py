from fastapi import APIRouter

from backend.schemas.cv_schemas import (
    CVMatchRequest,
    CVMatchResult,
    SkillExtractionRequest,
    SkillExtractionResponse,
    SkillGapRequest,
    SkillGapResponse,
)
from backend.services.cv_service import (
    analyse_skill_gap,
    extract_skills_from_cv,
    match_cv_to_jobs,
)

router = APIRouter(prefix="/cv", tags=["CV Intelligence"])


@router.post("/extract-skills", response_model=SkillExtractionResponse)
def cv_extract_skills(payload: SkillExtractionRequest):
    return extract_skills_from_cv(payload.text)


@router.post("/match-jobs", response_model=list[CVMatchResult])
def cv_match_jobs(payload: CVMatchRequest):
    return match_cv_to_jobs(
        cv_text=payload.cv_text,
        top_n=payload.top_n,
    )


@router.post("/skill-gap", response_model=SkillGapResponse)
def cv_skill_gap(payload: SkillGapRequest):
    return analyse_skill_gap(
        cv_text=payload.cv_text,
        top_n=payload.top_n,
    )