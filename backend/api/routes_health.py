from fastapi import APIRouter

from backend.services.ml_service import get_model_status
from skilllens.config import APP_NAME
from skilllens.analytics import run_basic_sql_healthcheck

router = APIRouter(tags=["Health"])


@router.get("/")
def root():
    return {
        "app": APP_NAME,
        "status": "running",
        "stage": "Stage 3 backend architecture",
    }


@router.get("/health")
def health():
    return {
        "status": "ok",
        "database_connection": run_basic_sql_healthcheck(),
        "models": get_model_status(),
    }