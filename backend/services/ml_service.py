from fastapi import HTTPException

from skilllens.ml.model_utils import (
    CATEGORY_MODEL_PATH,
    SALARY_MODEL_PATH,
    model_exists,
)
from skilllens.ml.train_category_model import predict_category
from skilllens.ml.train_salary_model import predict_salary


def get_model_status() -> dict:
    """
    Return whether trained model artefacts exist.
    """
    return {
        "salary_model_available": model_exists(SALARY_MODEL_PATH),
        "category_model_available": model_exists(CATEGORY_MODEL_PATH),
    }


def predict_salary_service(
    category: str,
    experience_level: str,
    work_type: str,
    location: str,
    skill_count: int,
) -> dict:
    """
    Predict salary range using trained salary model.
    """
    if not model_exists(SALARY_MODEL_PATH):
        raise HTTPException(
            status_code=404,
            detail="Salary model not found. Run: python -m skilllens.ml.train_salary_model",
        )

    salary = predict_salary(
        category=category,
        experience_level=experience_level,
        work_type=work_type,
        location=location,
        skill_count=skill_count,
    )

    return {
        "predicted_salary_midpoint": salary,
        "estimated_lower_range": round(salary * 0.92, 2),
        "estimated_upper_range": round(salary * 1.08, 2),
    }


def predict_category_service(text: str) -> dict:
    """
    Predict job category from job text.
    """
    cleaned = text.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    if not model_exists(CATEGORY_MODEL_PATH):
        raise HTTPException(
            status_code=404,
            detail="Category model not found. Run: python -m skilllens.ml.train_category_model",
        )

    category = predict_category(cleaned)

    return {
        "predicted_category": category,
    }