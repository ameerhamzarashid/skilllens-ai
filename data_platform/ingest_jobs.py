import pandas as pd
from sqlalchemy.exc import IntegrityError

from skilllens.config import SAMPLE_JOBS_PATH
from skilllens.database import SessionLocal, create_tables
from skilllens.models import JobPosting
from skilllens.skill_extractor import extract_skills, skills_to_string


def load_raw_jobs(path=SAMPLE_JOBS_PATH) -> pd.DataFrame:
    """
    Load raw job CSV.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Sample jobs file not found at {path}. "
            "Run: python -m data_platform.generate_sample_jobs"
        )

    return pd.read_csv(path)


def clean_jobs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and enrich raw job data.
    """
    cleaned = df.copy()

    text_columns = [
        "job_id",
        "title",
        "company",
        "location",
        "country",
        "category",
        "experience_level",
        "work_type",
        "salary_currency",
        "description",
        "posted_date",
        "source",
    ]

    for col in text_columns:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].fillna("").astype(str).str.strip()

    numeric_columns = ["salary_min", "salary_max"]

    for col in numeric_columns:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned["extracted_skills"] = cleaned["description"].apply(
        lambda text: skills_to_string(extract_skills(text))
    )

    cleaned = cleaned.drop_duplicates(subset=["job_id"])

    return cleaned


def ingest_dataframe(df: pd.DataFrame) -> int:
    """
    Insert cleaned jobs into database.
    """
    create_tables()

    inserted = 0

    with SessionLocal() as session:
        for _, row in df.iterrows():
            job = JobPosting(
                job_id=row["job_id"],
                title=row["title"],
                company=row["company"],
                location=row["location"],
                country=row["country"],
                category=row["category"],
                experience_level=row["experience_level"],
                work_type=row["work_type"],
                salary_min=float(row["salary_min"])
                if pd.notna(row["salary_min"])
                else None,
                salary_max=float(row["salary_max"])
                if pd.notna(row["salary_max"])
                else None,
                salary_currency=row["salary_currency"],
                description=row["description"],
                extracted_skills=row["extracted_skills"],
                posted_date=row["posted_date"],
                source=row["source"],
            )

            session.add(job)

            try:
                session.commit()
                inserted += 1
            except IntegrityError:
                session.rollback()

    return inserted


def main():
    raw_df = load_raw_jobs()
    clean_df = clean_jobs(raw_df)

    inserted = ingest_dataframe(clean_df)

    print("SkillLens AI Stage 1 ingestion complete.")
    print(f"Rows in raw file: {len(raw_df)}")
    print(f"Rows inserted: {inserted}")


if __name__ == "__main__":
    main()