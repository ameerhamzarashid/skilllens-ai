# SkillLens AI

SkillLens AI is a Workforce Intelligence and Career Analytics Platform.

It is designed as a full-stack data and AI project that demonstrates data engineering, data analytics, databases, backend APIs, machine learning readiness, dashboarding and system architecture.

This is Stage 1 of the project.

---

## Stage 1 Features

- Sample job dataset generator
- Job market data cleaning
- Rule-based skill extraction
- PostgreSQL-ready database layer
- SQLite fallback for beginner local setup
- SQLAlchemy ORM models
- Data ingestion pipeline
- Workforce analytics functions
- FastAPI backend foundation
- Streamlit market intelligence dashboard
- Basic tests with Pytest

---

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python |
| Data Handling | Pandas, NumPy |
| Database | PostgreSQL, SQLite fallback |
| ORM | SQLAlchemy |
| Backend API | FastAPI |
| Dashboard | Streamlit |
| Visualisation | Plotly |
| Testing | Pytest |
| Container Database | Docker Compose |

---

## Project Structure

```text
skilllens-ai/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── skilllens/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── skill_extractor.py
│   └── analytics.py
│
├── backend/
│   ├── __init__.py
│   └── main.py
│
├── dashboards/
│   ├── __init__.py
│   └── streamlit_app.py
│
├── data_platform/
│   ├── __init__.py
│   ├── generate_sample_jobs.py
│   └── ingest_jobs.py
│
├── data/
│   ├── raw/
│   └── processed/
│
└── tests/
    └── test_skill_extractor.py
    ---

## Stage 2 Features

Stage 2 adds the machine learning and intelligence layer.

### Added Capabilities

- Salary prediction model
- Job category classification model
- CV skill extraction
- CV-to-job matching
- Skill gap analysis
- Learning roadmap generation
- Streamlit ML pages
- FastAPI ML endpoints
- Model reports
- Additional tests

### Stage 2 Commands

Generate and ingest data:

```bash
python -m data_platform.generate_sample_jobs
python -m data_platform.ingest_jobs