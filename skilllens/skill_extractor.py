import re
from collections import Counter

from skilllens.config import TECH_SKILLS


def normalise_text(text: str) -> str:
    """
    Lowercase and clean text for skill matching.
    """
    if text is None:
        return ""

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_skills(text: str) -> list[str]:
    """
    Extract known technical skills from a job description.

    This is Stage 1 rule-based extraction.
    Later we can upgrade this using embeddings or NER.
    """
    cleaned = normalise_text(text)

    found = []

    for skill in TECH_SKILLS:
        skill_clean = normalise_text(skill)

        pattern = r"(?<!\w)" + re.escape(skill_clean) + r"(?!\w)"

        if re.search(pattern, cleaned):
            found.append(skill)

    return sorted(set(found))


def skills_to_string(skills: list[str]) -> str:
    """
    Convert list of skills to comma-separated string.
    """
    return ", ".join(sorted(set(skills)))


def string_to_skills(skills_text: str) -> list[str]:
    """
    Convert comma-separated skill text back to list.
    """
    if not skills_text:
        return []

    return [item.strip() for item in skills_text.split(",") if item.strip()]


def skill_frequency_from_texts(texts: list[str]) -> list[dict]:
    """
    Count skill frequency across many text fields.
    """
    counter = Counter()

    for text in texts:
        skills = extract_skills(text)

        for skill in skills:
            counter[skill] += 1

    return [
        {"skill": skill, "count": count}
        for skill, count in counter.most_common()
    ]