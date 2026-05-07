import json
from pathlib import Path

import pandas as pd

from skilllens.config import ML_REPORT_DIR, SAMPLE_JOBS_PATH
from skilllens.analytics import load_jobs_from_database
from skilllens.skill_extractor import string_to_skills


QUALITY_REPORT_PATH = ML_REPORT_DIR / "data_quality_report.json"


REQUIRED_COLUMNS = [
    "job_id",
    "title",
    "company",
    "location",
    "country",
    "category",
    "experience_level",
    "work_type",
    "salary_min",
    "salary_max",
    "description",
    "posted_date",
]


def load_quality_dataframe() -> pd.DataFrame:
    """
    Load data from database first.
    If database is empty, use sample CSV.
    """
    df = load_jobs_from_database()

    if not df.empty:
        return df

    if SAMPLE_JOBS_PATH.exists():
        return pd.read_csv(SAMPLE_JOBS_PATH)

    return pd.DataFrame()


def check_required_columns(df: pd.DataFrame) -> dict:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    return {
        "check": "required_columns",
        "passed": len(missing) == 0,
        "missing_columns": missing,
    }


def check_no_empty_required_values(df: pd.DataFrame) -> dict:
    details = {}

    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            details[col] = int(df[col].isna().sum())

    failed_columns = [col for col, count in details.items() if count > 0]

    return {
        "check": "no_empty_required_values",
        "passed": len(failed_columns) == 0,
        "null_counts": details,
        "failed_columns": failed_columns,
    }


def check_unique_job_ids(df: pd.DataFrame) -> dict:
    if "job_id" not in df.columns:
        return {
            "check": "unique_job_ids",
            "passed": False,
            "duplicate_count": None,
        }

    duplicate_count = int(df["job_id"].duplicated().sum())

    return {
        "check": "unique_job_ids",
        "passed": duplicate_count == 0,
        "duplicate_count": duplicate_count,
    }


def check_salary_validity(df: pd.DataFrame) -> dict:
    required = ["salary_min", "salary_max"]

    if any(col not in df.columns for col in required):
        return {
            "check": "salary_validity",
            "passed": False,
            "reason": "salary_min or salary_max missing",
        }

    salary_min = pd.to_numeric(df["salary_min"], errors="coerce")
    salary_max = pd.to_numeric(df["salary_max"], errors="coerce")

    invalid_min = int((salary_min <= 0).sum())
    invalid_max = int((salary_max <= 0).sum())
    min_greater_than_max = int((salary_min > salary_max).sum())

    passed = invalid_min == 0 and invalid_max == 0 and min_greater_than_max == 0

    return {
        "check": "salary_validity",
        "passed": passed,
        "invalid_min_count": invalid_min,
        "invalid_max_count": invalid_max,
        "min_greater_than_max_count": min_greater_than_max,
    }


def check_extracted_skills(df: pd.DataFrame) -> dict:
    if "extracted_skills" not in df.columns:
        return {
            "check": "extracted_skills",
            "passed": False,
            "reason": "extracted_skills column missing",
        }

    empty_skill_rows = 0

    for value in df["extracted_skills"].fillna(""):
        if len(string_to_skills(value)) == 0:
            empty_skill_rows += 1

    passed = empty_skill_rows < len(df) * 0.2

    return {
        "check": "extracted_skills",
        "passed": passed,
        "empty_skill_rows": int(empty_skill_rows),
        "total_rows": int(len(df)),
    }


def run_data_quality_checks() -> dict:
    """
    Run all quality checks and save a report.
    """
    ML_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_quality_dataframe()

    if df.empty:
        report = {
            "overall_passed": False,
            "row_count": 0,
            "checks": [
                {
                    "check": "data_available",
                    "passed": False,
                    "reason": "No data found",
                }
            ],
        }

        QUALITY_REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

    checks = [
        check_required_columns(df),
        check_no_empty_required_values(df),
        check_unique_job_ids(df),
        check_salary_validity(df),
        check_extracted_skills(df),
    ]

    overall_passed = all(check["passed"] for check in checks)

    report = {
        "overall_passed": overall_passed,
        "row_count": int(len(df)),
        "checks": checks,
    }

    QUALITY_REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    return report


def main():
    report = run_data_quality_checks()

    print("SkillLens AI data quality report")
    print(json.dumps(report, indent=2))

    if not report["overall_passed"]:
        raise SystemExit("Data quality checks failed.")


if __name__ == "__main__":
    main()