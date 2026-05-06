from skilllens.skill_extractor import extract_skills, normalise_text


def test_normalise_text():
    text = "Python, SQL & Power BI!"
    cleaned = normalise_text(text)

    assert "python" in cleaned
    assert "sql" in cleaned
    assert "power bi" in cleaned


def test_extract_skills():
    text = """
    We need a Data Scientist with Python, SQL, machine learning,
    Pandas, Docker and FastAPI experience.
    """

    skills = extract_skills(text)

    assert "python" in skills
    assert "sql" in skills
    assert "machine learning" in skills
    assert "pandas" in skills
    assert "docker" in skills
    assert "fastapi" in skills