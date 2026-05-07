import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

SAMPLE_JOBS_PATH = RAW_DATA_DIR / "sample_jobs.csv"

ML_DIR = PROJECT_ROOT / "ml"
MODEL_DIR = ML_DIR / "models"
ML_REPORT_DIR = ML_DIR / "reports"

APP_NAME = os.getenv("APP_NAME", "SkillLens AI")
APP_ENV = os.getenv("APP_ENV", "development")

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

ROADMAP_LIBRARY = {
    "python": [
        "Practise Python fundamentals with Pandas and NumPy.",
        "Build one clean data analysis notebook using real or generated data.",
    ],
    "sql": [
        "Practise joins, CTEs, window functions and aggregations.",
        "Create a small PostgreSQL database and write analytical queries.",
    ],
    "power bi": [
        "Build an interactive dashboard with slicers, measures and KPI cards.",
        "Practise DAX basics and dashboard storytelling.",
    ],
    "tableau": [
        "Build a role-based dashboard and practise calculated fields.",
    ],
    "machine learning": [
        "Train classification and regression models using scikit-learn.",
        "Evaluate models with proper train-test split and metrics.",
    ],
    "deep learning": [
        "Practise neural network basics using TensorFlow or PyTorch.",
        "Build a small image or text classification model.",
    ],
    "fastapi": [
        "Create REST endpoints for model inference.",
        "Add Pydantic schemas and API documentation.",
    ],
    "docker": [
        "Containerise a Python app with Docker.",
        "Write a docker-compose file for app plus database.",
    ],
    "airflow": [
        "Create a simple DAG for extracting, transforming and loading data.",
    ],
    "dbt": [
        "Create staging and mart models using dbt.",
        "Add tests for not null, unique and accepted values.",
    ],
    "mlflow": [
        "Track model experiments, parameters and metrics.",
        "Save the best model as an artefact.",
    ],
    "spark": [
        "Practise distributed data processing with PySpark DataFrames.",
    ],
    "azure": [
        "Learn Azure Storage, Azure SQL and basic deployment workflows.",
    ],
    "aws": [
        "Learn S3, RDS and basic cloud deployment workflows.",
    ],
    "gcp": [
        "Learn BigQuery and Cloud Storage basics.",
    ],
    "llm": [
        "Build a small LLM-powered assistant using prompt engineering.",
    ],
    "rag": [
        "Create a retrieval pipeline using embeddings and a vector database.",
    ],
    "langchain": [
        "Build a document Q&A pipeline with LangChain.",
    ],
}