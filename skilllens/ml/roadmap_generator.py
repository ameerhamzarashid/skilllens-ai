from skilllens.config import ROADMAP_LIBRARY


def generate_learning_roadmap(missing_skills: list[str], max_skills: int = 6) -> list[dict]:
    """
    Generate a simple personalised learning roadmap from missing skills.
    """
    roadmap = []

    priority_skills = missing_skills[:max_skills]

    for index, skill in enumerate(priority_skills, start=1):
        skill_key = skill.lower().strip()

        steps = ROADMAP_LIBRARY.get(
            skill_key,
            [
                f"Study the fundamentals of {skill}.",
                f"Build a small portfolio task using {skill}.",
            ],
        )

        roadmap.append(
            {
                "priority": index,
                "skill": skill,
                "learning_steps": steps,
                "portfolio_task": portfolio_task_for_skill(skill_key),
            }
        )

    return roadmap


def portfolio_task_for_skill(skill: str) -> str:
    """
    Suggest a project task for a missing skill.
    """
    tasks = {
        "python": "Create a clean data processing script with functions, logging and tests.",
        "sql": "Build a database with at least three tables and write analytical SQL queries.",
        "power bi": "Create a Power BI dashboard with KPIs, filters and business insights.",
        "machine learning": "Train and evaluate a classification or regression model.",
        "fastapi": "Deploy a model behind a FastAPI endpoint.",
        "docker": "Containerise a Python app and run it with Docker Compose.",
        "airflow": "Create an Airflow DAG that ingests and transforms data.",
        "dbt": "Create staging and mart models with tests and documentation.",
        "mlflow": "Track model experiments and save the best model artefact.",
        "llm": "Build a prompt-based assistant for summarising documents.",
        "rag": "Build a small retrieval-augmented generation pipeline.",
    }

    return tasks.get(
        skill,
        f"Build a mini project that demonstrates practical use of {skill}.",
    )


def roadmap_to_markdown(roadmap: list[dict]) -> str:
    """
    Convert roadmap list into markdown.
    """
    if not roadmap:
        return "No major missing skills found. Focus on strengthening existing projects."

    lines = []

    for item in roadmap:
        lines.append(f"### Priority {item['priority']}: {item['skill'].title()}")
        lines.append("")
        lines.append("Learning steps:")

        for step in item["learning_steps"]:
            lines.append(f"- {step}")

        lines.append("")
        lines.append(f"Portfolio task: {item['portfolio_task']}")
        lines.append("")

    return "\n".join(lines)