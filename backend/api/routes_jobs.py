from fastapi import APIRouter, Query

from backend.schemas.job_schemas import (
    CategoryCountResponse,
    JobPostingResponse,
    JobSummaryResponse,
    SalaryByCategoryResponse,
)
from backend.services.job_service import (
    get_category_distribution,
    get_jobs_summary,
    get_salary_by_category,
    list_jobs,
)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/summary", response_model=JobSummaryResponse)
def jobs_summary():
    return get_jobs_summary()


@router.get("", response_model=list[JobPostingResponse])
def jobs(
    limit: int = Query(default=20, ge=1, le=500),
):
    return list_jobs(limit=limit)


@router.get("/categories", response_model=list[CategoryCountResponse])
def categories():
    return get_category_distribution()


@router.get("/salary-by-category", response_model=list[SalaryByCategoryResponse])
def salary_categories():
    return get_salary_by_category()