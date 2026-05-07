from fastapi import APIRouter, Query

from backend.schemas.cv_schemas import (
    SkillExtractionRequest,
    SkillExtractionResponse,
)
from backend.schemas.job_schemas import SkillCountResponse
from backend.services.cv_service import extract_skills_from_text
from backend.services.job_service import get_top_skills

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("/top", response_model=list[SkillCountResponse])
def top_skills(
    limit: int = Query(default=20, ge=1, le=100),
):
    return get_top_skills(limit=limit)


@router.post("/extract", response_model=SkillExtractionResponse)
def extract_skills(payload: SkillExtractionRequest):
    return extract_skills_from_text(payload.text)