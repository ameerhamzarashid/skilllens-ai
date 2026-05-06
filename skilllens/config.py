import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

SAMPLE_JOBS_PATH = RAW_DATA_DIR / "sample_jobs.csv"

APP_NAME = os.getenv("APP_NAME", "SkillLens AI")
APP_ENV = os.getenv("APP_ENV", "development")

# If .env has DATABASE_URL, use PostgreSQL.
# If not, use SQLite fallback so the beginner setup still runs.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{PROJECT_ROOT / 'skilllens_stage1.db'}",
)

TECH_SKILLS = [
    "python",
    "sql",
    "r",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "keras",
    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",
    "fastapi",
    "flask",
    "django",
    "postgresql",
    "mysql",
    "mongodb",
    "snowflake",
    "databricks",
    "spark",
    "apache spark",
    "airflow",
    "prefect",
    "dbt",
    "docker",
    "kubernetes",
    "mlflow",
    "git",
    "github actions",
    "azure",
    "aws",
    "gcp",
    "linux",
    "bash",
    "etl",
    "elt",
    "data warehouse",
    "data lake",
    "data modelling",
    "statistics",
    "a/b testing",
    "time series",
    "forecasting",
    "llm",
    "rag",
    "langchain",
    "openai",
    "vector database",
    "chromadb",
    "pinecone",
]

JOB_CATEGORIES = [
    "Data Analyst",
    "Data Scientist",
    "Data Engineer",
    "Machine Learning Engineer",
    "BI Analyst",
    "Analytics Engineer",
    "AI Engineer",
]