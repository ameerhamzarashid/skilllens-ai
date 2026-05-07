import re

import pandas as pd

from skilllens.skill_extractor import extract_skills, string_to_skills


def clean_cv_text(text: str) -> str:
    """
    Clean CV text for matching.
    """
    if text is None:
        return ""

    text = str(text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_cv_skills(cv_text: str) -> list[str]:
    """
    Extract skills from CV text.
    """
    cleaned = clean_cv_text(cv_text)
    return extract_skills(cleaned)


def calculate_skill_match_score(
    cv_skills: list[str],
    job_skills: list[str],
) -> dict:
    """
    Calculate CV-to-job skill match score.
    """
    cv_set = set(skill.lower().strip() for skill in cv_skills)
    job_set = set(skill.lower().strip() for skill in job_skills)

    if not job_set:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "extra_cv_skills": sorted(cv_set),
            "required_skill_count": 0,
            "matched_skill_count": 0,
        }

    matched = sorted(cv_set.intersection(job_set))
    missing = sorted(job_set.difference(cv_set))
    extra = sorted(cv_set.difference(job_set))

    score = len(matched) / len(job_set) * 100

    return {
        "match_score": round(float(score), 2),
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_cv_skills": extra,
        "required_skill_count": len(job_set),
        "matched_skill_count": len(matched),
    }


def match_cv_to_job(cv_text: str, job_row: pd.Series | dict) -> dict:
    """
    Match CV text to one job posting.
    """
    cv_skills = extract_cv_skills(cv_text)

    if isinstance(job_row, pd.Series):
        job_data = job_row.to_dict()
    else:
        job_data = dict(job_row)

    job_skills = string_to_skills(job_data.get("extracted_skills", ""))

    result = calculate_skill_match_score(cv_skills, job_skills)

    result.update(
        {
            "job_id": job_data.get("job_id"),
            "title": job_data.get("title"),
            "company": job_data.get("company"),
            "location": job_data.get("location"),
            "category": job_data.get("category"),
            "cv_skills": cv_skills,
            "job_skills": job_skills,
        }
    )

    return result


def rank_jobs_for_cv(
    cv_text: str,
    jobs_df: pd.DataFrame,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Rank all jobs by CV match score.
    """
    if jobs_df.empty:
        return pd.DataFrame()

    rows = []

    for _, row in jobs_df.iterrows():
        match = match_cv_to_job(cv_text, row)
        rows.append(match)

    out = pd.DataFrame(rows)

    if out.empty:
        return out

    out["matched_skills_text"] = out["matched_skills"].apply(
        lambda skills: ", ".join(skills)
    )

    out["missing_skills_text"] = out["missing_skills"].apply(
        lambda skills: ", ".join(skills)
    )

    return (
        out.sort_values(
            ["match_score", "matched_skill_count"],
            ascending=False,
        )
        .head(top_n)
        .reset_index(drop=True)
    )


def skill_gap_summary(cv_text: str, jobs_df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise most common missing skills across matching jobs.
    """
    ranked = rank_jobs_for_cv(cv_text, jobs_df, top_n=len(jobs_df))

    if ranked.empty:
        return pd.DataFrame(columns=["skill", "missing_count"])

    missing_rows = []

    for _, row in ranked.iterrows():
        for skill in row["missing_skills"]:
            missing_rows.append({"skill": skill})

    if not missing_rows:
        return pd.DataFrame(columns=["skill", "missing_count"])

    return (
        pd.DataFrame(missing_rows)
        .value_counts("skill")
        .reset_index(name="missing_count")
        .sort_values("missing_count", ascending=False)
    )