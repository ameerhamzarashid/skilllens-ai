from skilllens.ml.cv_matcher import (
    calculate_skill_match_score,
    extract_cv_skills,
)


def test_extract_cv_skills():
    cv_text = "I have experience with Python, SQL, Power BI, Docker and FastAPI."

    skills = extract_cv_skills(cv_text)

    assert "python" in skills
    assert "sql" in skills
    assert "power bi" in skills
    assert "docker" in skills
    assert "fastapi" in skills


def test_calculate_skill_match_score():
    cv_skills = ["python", "sql", "power bi"]
    job_skills = ["python", "sql", "docker", "fastapi"]

    result = calculate_skill_match_score(cv_skills, job_skills)

    assert result["match_score"] == 50.0
    assert "python" in result["matched_skills"]
    assert "docker" in result["missing_skills"]