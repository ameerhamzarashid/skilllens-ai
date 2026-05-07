from pydantic import BaseModel


class JobSummaryResponse(BaseModel):
    total_jobs: int
    companies: int
    locations: int
    avg_salary: float
    skills: int


class JobPostingResponse(BaseModel):
    job_id: str | None = None
    title: str | None = None
    company: str | None = None
    location: str | None = None
    country: str | None = None
    category: str | None = None
    experience_level: str | None = None
    work_type: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str | None = None
    extracted_skills: str | None = None
    posted_date: str | None = None
    source: str | None = None


class SkillCountResponse(BaseModel):
    skill: str
    count: int


class CategoryCountResponse(BaseModel):
    category: str
    count: int


class SalaryByCategoryResponse(BaseModel):
    category: str
    avg_salary: float