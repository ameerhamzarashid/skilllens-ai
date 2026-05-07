import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from skilllens.analytics import load_jobs_from_database
from skilllens.config import MODEL_DIR, ML_REPORT_DIR, SAMPLE_JOBS_PATH
from skilllens.skill_extractor import extract_skills, skills_to_string


SALARY_MODEL_PATH = MODEL_DIR / "salary_model.joblib"
SALARY_FEATURES_PATH = MODEL_DIR / "salary_features.joblib"
SALARY_REPORT_PATH = ML_REPORT_DIR / "salary_model_report.json"

CATEGORY_MODEL_PATH = MODEL_DIR / "category_model.joblib"
CATEGORY_REPORT_PATH = ML_REPORT_DIR / "category_model_report.json"


def ensure_ml_dirs() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    ML_REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_training_jobs() -> pd.DataFrame:
    """
    Load jobs from database first.
    If database is empty, load sample CSV.
    """
    df = load_jobs_from_database()

    if not df.empty:
        return df

    if SAMPLE_JOBS_PATH.exists():
        df = pd.read_csv(SAMPLE_JOBS_PATH)

        if "extracted_skills" not in df.columns:
            df["extracted_skills"] = df["description"].apply(
                lambda text: skills_to_string(extract_skills(text))
            )

        return df

    return pd.DataFrame()


def salary_midpoint(df: pd.DataFrame) -> pd.Series:
    """
    Calculate salary midpoint.
    """
    return (df["salary_min"] + df["salary_max"]) / 2


def save_json_report(report: dict[str, Any], path: Path) -> None:
    ensure_ml_dirs()

    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)


def load_json_report(path: Path) -> dict:
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_model(model: Any, path: Path) -> None:
    ensure_ml_dirs()
    joblib.dump(model, path)


def load_model(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path}")

    return joblib.load(path)


def model_exists(path: Path) -> bool:
    return path.exists()