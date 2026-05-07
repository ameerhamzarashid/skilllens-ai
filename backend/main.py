from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes_cv import router as cv_router
from backend.api.routes_health import router as health_router
from backend.api.routes_jobs import router as jobs_router
from backend.api.routes_ml import router as ml_router
from backend.api.routes_skills import router as skills_router

app = FastAPI(
    title="SkillLens AI API",
    description=(
        "Backend API for workforce intelligence, career analytics, "
        "CV matching, skill gap analysis and ML-powered salary prediction."
    ),
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(jobs_router)
app.include_router(skills_router)
app.include_router(cv_router)
app.include_router(ml_router)