from fastapi import APIRouter

from backend.schemas.ml_schemas import (
    CategoryPredictionRequest,
    CategoryPredictionResponse,
    ModelStatusResponse,
    SalaryPredictionRequest,
    SalaryPredictionResponse,
)
from backend.services.ml_service import (
    get_model_status,
    predict_category_service,
    predict_salary_service,
)

router = APIRouter(prefix="/ml", tags=["Machine Learning"])


@router.get("/status", response_model=ModelStatusResponse)
def model_status():
    return get_model_status()


@router.post("/predict-salary", response_model=SalaryPredictionResponse)
def predict_salary(payload: SalaryPredictionRequest):
    return predict_salary_service(
        category=payload.category,
        experience_level=payload.experience_level,
        work_type=payload.work_type,
        location=payload.location,
        skill_count=payload.skill_count,
    )


@router.post("/predict-category", response_model=CategoryPredictionResponse)
def predict_category(payload: CategoryPredictionRequest):
    return predict_category_service(payload.text)