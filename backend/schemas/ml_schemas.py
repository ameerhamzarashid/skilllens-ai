from pydantic import BaseModel, Field


class SalaryPredictionRequest(BaseModel):
    category: str = Field(..., description="Job category, for example Data Scientist.")
    experience_level: str = Field(..., description="Experience level.")
    work_type: str = Field(..., description="Remote, Hybrid or Onsite.")
    location: str = Field(..., description="Job location.")
    skill_count: int = Field(..., ge=0, le=50, description="Number of relevant skills.")


class SalaryPredictionResponse(BaseModel):
    predicted_salary_midpoint: float
    estimated_lower_range: float
    estimated_upper_range: float


class CategoryPredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Job title or description text.")


class CategoryPredictionResponse(BaseModel):
    predicted_category: str


class ModelStatusResponse(BaseModel):
    salary_model_available: bool
    category_model_available: bool