import random
from datetime import datetime, timedelta

import pandas as pd

from skilllens.config import JOB_CATEGORIES, RAW_DATA_DIR, SAMPLE_JOBS_PATH

random.seed(42)


COMPANIES = [
    "NorthStar Analytics",
    "CloudNova Systems",
    "DataBridge Labs",
    "InsightWorks",
    "FinEdge AI",
    "HealthMetric Solutions",
    "RetailPulse",
    "GridCore Energy",
    "UrbanData Studio",
    "TalentSphere",
]

LOCATIONS = [
    "London",
    "Newcastle",
    "Manchester",
    "Edinburgh",
    "Glasgow",
    "Birmingham",
    "Leeds",
    "Bristol",
    "Remote UK",
]

COUNTRIES = ["United Kingdom"]

EXPERIENCE_LEVELS = [
    "Entry Level",
    "Junior",
    "Mid Level",
    "Senior",
]

WORK_TYPES = [
    "Remote",
    "Hybrid",
    "Onsite",
]

CATEGORY_SKILLS = {
    "Data Analyst": [
        "sql",
        "excel",
        "power bi",
        "tableau",
        "python",
        "statistics",
        "data modelling",
    ],
    "Data Scientist": [
        "python",
        "sql",
        "machine learning",
        "statistics",
        "scikit-learn",
        "pandas",
        "numpy",
        "forecasting",
    ],
    "Data Engineer": [
        "python",
        "sql",
        "spark",
        "airflow",
        "etl",
        "data warehouse",
        "postgresql",
        "docker",
    ],
    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "pytorch",
        "tensorflow",
        "mlflow",
        "docker",
        "fastapi",
    ],
    "BI Analyst": [
        "sql",
        "power bi",
        "tableau",
        "excel",
        "data modelling",
        "statistics",
    ],
    "Analytics Engineer": [
        "sql",
        "dbt",
        "data warehouse",
        "snowflake",
        "python",
        "git",
        "etl",
    ],
    "AI Engineer": [
        "python",
        "llm",
        "rag",
        "langchain",
        "openai",
        "vector database",
        "fastapi",
        "docker",
    ],
}

EXTRA_SKILLS = [
    "azure",
    "aws",
    "gcp",
    "kubernetes",
    "github actions",
    "linux",
    "bash",
    "time series",
    "a/b testing",
    "databricks",
    "mongodb",
    "mysql",
    "chromadb",
    "pinecone",
]


def build_description(category: str, skills: list[str]) -> str:
    """
    Create a realistic job description.
    """
    intro = {
        "Data Analyst": "You will deliver dashboards, reporting pipelines and business insight for stakeholders.",
        "Data Scientist": "You will build predictive models, analyse complex datasets and communicate insights.",
        "Data Engineer": "You will design data pipelines, transform raw data and maintain data platforms.",
        "Machine Learning Engineer": "You will deploy machine learning models and build production inference services.",
        "BI Analyst": "You will create business intelligence reports and support performance tracking.",
        "Analytics Engineer": "You will transform data into trusted analytics models and maintain the semantic layer.",
        "AI Engineer": "You will build AI applications using LLMs, retrieval pipelines and backend services.",
    }[category]

    skill_sentence = "The role requires experience with " + ", ".join(skills) + "."

    responsibility = (
        "You will work with cross-functional teams, document requirements, "
        "improve data quality, and turn business problems into reliable data products."
    )

    return f"{intro} {skill_sentence} {responsibility}"


def salary_range(category: str, level: str) -> tuple[int, int]:
    """
    Generate realistic UK salary ranges for sample data.
    """
    base = {
        "Data Analyst": 32000,
        "BI Analyst": 34000,
        "Data Scientist": 42000,
        "Data Engineer": 45000,
        "Analytics Engineer": 47000,
        "Machine Learning Engineer": 52000,
        "AI Engineer": 55000,
    }[category]

    level_boost = {
        "Entry Level": 0,
        "Junior": 5000,
        "Mid Level": 14000,
        "Senior": 28000,
    }[level]

    salary_min = base + level_boost + random.randint(-3000, 3000)
    salary_max = salary_min + random.randint(6000, 18000)

    return salary_min, salary_max


def generate_sample_jobs(num_jobs: int = 350) -> pd.DataFrame:
    """
    Generate synthetic job posting data.
    """
    rows = []

    start_date = datetime.today() - timedelta(days=180)

    for i in range(1, num_jobs + 1):
        category = random.choice(JOB_CATEGORIES)
        company = random.choice(COMPANIES)
        location = random.choice(LOCATIONS)
        country = random.choice(COUNTRIES)
        level = random.choice(EXPERIENCE_LEVELS)
        work_type = random.choice(WORK_TYPES)

        core_skills = random.sample(
            CATEGORY_SKILLS[category],
            k=min(5, len(CATEGORY_SKILLS[category])),
        )

        optional_skills = random.sample(EXTRA_SKILLS, k=random.randint(1, 4))

        skills = sorted(set(core_skills + optional_skills))

        salary_min, salary_max = salary_range(category, level)

        posted_date = start_date + timedelta(days=random.randint(0, 180))

        title = f"{level} {category}"

        rows.append(
            {
                "job_id": f"JOB-{i:05d}",
                "title": title,
                "company": company,
                "location": location,
                "country": country,
                "category": category,
                "experience_level": level,
                "work_type": work_type,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "salary_currency": "GBP",
                "description": build_description(category, skills),
                "posted_date": posted_date.strftime("%Y-%m-%d"),
                "source": "synthetic_stage_1",
            }
        )

    return pd.DataFrame(rows)


def main():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_sample_jobs(num_jobs=350)
    df.to_csv(SAMPLE_JOBS_PATH, index=False)

    print(f"Sample job dataset created at: {SAMPLE_JOBS_PATH}")
    print(f"Rows: {len(df)}")


if __name__ == "__main__":
    main()