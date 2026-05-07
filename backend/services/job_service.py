from skilllens.analytics import (
    get_summary_metrics,
    jobs_by_category,
    load_jobs_from_database,
    salary_by_category,
    top_skills,
)


def get_jobs_dataframe():
    """
    Load jobs from the database.
    """
    return load_jobs_from_database()


def get_jobs_summary() -> dict:
    """
    Return headline job market metrics.
    """
    df = get_jobs_dataframe()

    if df.empty:
        return {
            "total_jobs": 0,
            "companies": 0,
            "locations": 0,
            "avg_salary": 0,
            "skills": 0,
        }

    return get_summary_metrics(df)


def list_jobs(limit: int = 20) -> list[dict]:
    """
    Return job postings.
    """
    df = get_jobs_dataframe()

    if df.empty:
        return []

    safe_limit = max(1, min(limit, 500))

    return df.head(safe_limit).to_dict(orient="records")


def get_top_skills(limit: int = 20) -> list[dict]:
    """
    Return most common extracted skills.
    """
    df = get_jobs_dataframe()

    if df.empty:
        return []

    safe_limit = max(1, min(limit, 100))

    return top_skills(df, top_n=safe_limit).to_dict(orient="records")


def get_category_distribution() -> list[dict]:
    """
    Return job counts by category.
    """
    df = get_jobs_dataframe()

    if df.empty:
        return []

    return jobs_by_category(df).to_dict(orient="records")


def get_salary_by_category() -> list[dict]:
    """
    Return average salary by category.
    """
    df = get_jobs_dataframe()

    if df.empty:
        return []

    return salary_by_category(df).round(2).to_dict(orient="records")