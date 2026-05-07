# SkillLens AI

**SkillLens AI** is a full-stack Workforce Intelligence and Career Analytics Platform.

It combines data engineering, databases, machine learning, backend APIs, frontend development, MLOps, and deployment-ready architecture into one complete portfolio project.

The platform helps users explore job market trends, analyse high-demand skills, match CVs to job postings, predict salary ranges, identify missing skills, and generate personalised learning roadmaps.

---

## Project Purpose

SkillLens AI was built to demonstrate the complete technical capability expected from a modern Data Scientist, Data Engineer, Data Analyst, System Analyst, ML Engineer, and Full-Stack Data Product Developer.

The project is not just a Python dashboard. It includes:

- Data generation
- Data ingestion
- Data cleaning
- Skill extraction
- Database modelling
- SQLAlchemy ORM
- PostgreSQL readiness
- Machine learning models
- CV-to-job matching
- Skill gap analysis
- FastAPI backend
- Modular API architecture
- Next.js frontend
- TypeScript interface
- Tailwind styling
- Docker full-stack setup
- Data quality checks
- CI/CD workflow
- MLOps documentation
- Deployment planning

---

## Main Features

### Workforce Market Intelligence

- Analyse job demand by role category
- View top hiring locations
- Compare remote, hybrid, and onsite roles
- Analyse average salary by role category
- Explore top in-demand skills
- Search job postings

### CV and Career Intelligence

- Paste CV text
- Extract CV skills
- Match CV against job postings
- Rank job opportunities by skill match score
- Show matched skills
- Show missing skills
- Generate skill gap analysis
- Create personalised learning roadmaps

### Machine Learning

- Salary prediction model
- Job category classification model
- Model training scripts
- Model artefact saving
- Model evaluation reports
- ML inference through API endpoints

### Backend API

- FastAPI backend
- Modular route structure
- Pydantic request and response schemas
- Service layer architecture
- Health checks
- Job analytics endpoints
- Skill extraction endpoints
- CV matching endpoints
- Salary prediction endpoint
- Job category prediction endpoint

### Full-Stack Frontend

- Next.js App Router frontend
- TypeScript
- Tailwind CSS
- Recharts visualisations
- API integration with FastAPI
- Market dashboard page
- CV matcher page
- Salary predictor page
- Skill gap roadmap page

### Data Engineering and MLOps

- Data quality checks
- End-to-end pipeline script
- Dockerised backend
- Dockerised frontend
- PostgreSQL Docker service
- Docker Compose setup
- GitHub Actions CI
- MLOps workflow documentation
- Deployment guide

---

## Tech Stack

| Area | Technology |
|---|---|
| Programming Language | Python |
| Data Handling | Pandas, NumPy |
| Database | PostgreSQL, SQLite fallback |
| ORM | SQLAlchemy |
| Backend API | FastAPI |
| API Validation | Pydantic |
| Dashboard | Streamlit |
| Frontend | Next.js |
| Frontend Language | TypeScript |
| Frontend Styling | Tailwind CSS |
| Charts | Plotly, Recharts |
| Machine Learning | scikit-learn |
| Model Saving | joblib |
| Testing | Pytest |
| Containerisation | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Deployment Ready For | Vercel, Render, Neon, Railway |

---

## Final Project Structure

```text
skilllens-ai/
│
├── README.md
├── SETUP_RUN_DEBUG.md
├── requirements.txt
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Makefile
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── Dockerfile
│   ├── .dockerignore
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes_health.py
│   │   ├── routes_jobs.py
│   │   ├── routes_skills.py
│   │   ├── routes_cv.py
│   │   └── routes_ml.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── cv_schemas.py
│   │   ├── job_schemas.py
│   │   └── ml_schemas.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── job_service.py
│       ├── cv_service.py
│       └── ml_service.py
│
├── dashboards/
│   ├── __init__.py
│   ├── streamlit_app.py
│   │
│   └── pages/
│       ├── 1_CV_Job_Matcher.py
│       ├── 2_Salary_Predictor.py
│       └── 3_Skill_Gap_Analysis.py
│
├── data_platform/
│   ├── __init__.py
│   ├── generate_sample_jobs.py
│   ├── ingest_jobs.py
│   ├── data_quality.py
│   └── run_pipeline.py
│
├── skilllens/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── skill_extractor.py
│   ├── analytics.py
│   │
│   └── ml/
│       ├── __init__.py
│       ├── model_utils.py
│       ├── train_salary_model.py
│       ├── train_category_model.py
│       ├── cv_matcher.py
│       └── roadmap_generator.py
│
├── frontend/
│   ├── README.md
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.local.example
│   ├── package.json
│   ├── next.config.ts
│   ├── postcss.config.mjs
│   ├── tsconfig.json
│   │
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── market/
│   │   │   └── page.tsx
│   │   ├── cv-match/
│   │   │   └── page.tsx
│   │   ├── salary/
│   │   │   └── page.tsx
│   │   └── skill-gap/
│   │       └── page.tsx
│   │
│   ├── components/
│   │   ├── Badge.tsx
│   │   ├── JobTable.tsx
│   │   ├── Navbar.tsx
│   │   ├── SectionCard.tsx
│   │   └── StatCard.tsx
│   │
│   └── lib/
│       ├── api.ts
│       ├── types.ts
│       └── utils.ts
│
├── data/
│   ├── raw/
│   └── processed/
│
├── ml/
│   ├── models/
│   └── reports/
│
├── reports/
│   ├── architecture.md
│   ├── api_documentation.md
│   ├── data_dictionary.md
│   ├── deployment_guide.md
│   ├── mlops_workflow.md
│   └── model_card.md
│
└── tests/
    ├── test_api_cv.py
    ├── test_api_health.py
    ├── test_cv_matcher.py
    └── test_skill_extractor.py
```

---

## Dataset

SkillLens AI uses generated sample job data. No external dataset is required for the current version.

The generated dataset contains synthetic job postings for:

- Data Analyst
- Data Scientist
- Data Engineer
- Machine Learning Engineer
- BI Analyst
- Analytics Engineer
- AI Engineer

Generate the dataset:

```bash
python -m data_platform.generate_sample_jobs
```

Output:

```text
data/raw/sample_jobs.csv
```

---

## Database

The project supports two database modes.

### SQLite Fallback

If no `.env` file exists, the project automatically uses local SQLite:

```text
skilllens_stage1.db
```

### PostgreSQL

For PostgreSQL, create `.env` from `.env.example` and set:

```env
DATABASE_URL=postgresql+psycopg2://skilllens_user:skilllens_password@localhost:5432/skilllens_db
```

Or use the Docker Compose PostgreSQL service.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ameerhamzarashid/skilllens-ai.git
cd skilllens-ai
```

### 2. Create Python Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

## Run the Data and ML Pipeline

From the root folder:

```bash
python -m data_platform.run_pipeline
```

This runs:

1. Generate sample job data
2. Ingest jobs into the database
3. Run data quality checks
4. Train salary prediction model
5. Train job category classification model
6. Run backend tests

---

## Manual Pipeline Commands

```bash
python -m data_platform.generate_sample_jobs
python -m data_platform.ingest_jobs
python -m data_platform.data_quality
python -m skilllens.ml.train_salary_model
python -m skilllens.ml.train_category_model
python -m pytest
```

---

## Run FastAPI Backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

---

## Run Streamlit Dashboard

From the project root:

```bash
streamlit run dashboards/streamlit_app.py
```

Streamlit app:

```text
http://localhost:8501
```

---

## Run Next.js Frontend

Open a second terminal:

```bash
cd frontend
copy .env.local.example .env.local
npm run dev
```

macOS or Linux:

```bash
cd frontend
cp .env.local.example .env.local
npm run dev
```

Frontend app:

```text
http://localhost:3000
```

Make sure the FastAPI backend is already running at:

```text
http://127.0.0.1:8000
```

---

## Run Full Stack with Docker

Make sure Docker Desktop is running.

From the project root:

```bash
docker compose up --build
```

Services:

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

Stop services:

```bash
docker compose down
```

Stop services and remove database volume:

```bash
docker compose down -v
```

---

## API Endpoints

### Health

```text
GET /
GET /health
```

### Jobs

```text
GET /jobs
GET /jobs/summary
GET /jobs/categories
GET /jobs/salary-by-category
```

### Skills

```text
GET /skills/top
POST /skills/extract
```

### CV Intelligence

```text
POST /cv/extract-skills
POST /cv/match-jobs
POST /cv/skill-gap
```

### Machine Learning

```text
GET /ml/status
POST /ml/predict-salary
POST /ml/predict-category
```

---

## Frontend Pages

```text
/              Home
/market        Market Intelligence
/cv-match      CV Job Matcher
/salary        Salary Predictor
/skill-gap     Skill Gap Roadmap
```

---

## Testing

Run all Python tests:

```bash
python -m pytest
```

Build frontend:

```bash
cd frontend
npm run build
```

---

## GitHub Actions CI

The project includes:

```text
.github/workflows/ci.yml
```

The CI workflow runs on push and pull request to `main`.

It performs:

- Python dependency installation
- Data generation
- Data ingestion
- Data quality checks
- Salary model training
- Category model training
- Pytest execution
- Frontend build

---

## Deployment Architecture

Recommended deployment setup:

```text
Frontend: Vercel
Backend API: Render or Railway
Database: Neon PostgreSQL, Render PostgreSQL, or Railway PostgreSQL
```

Recommended portfolio setup:

```text
Next.js frontend on Vercel
FastAPI backend on Render
PostgreSQL database on Neon
```

Frontend environment variable:

```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.com
```

Backend environment variable:

```env
DATABASE_URL=postgresql+psycopg2://username:password@host/dbname?sslmode=require
```

---

## Project Stages

### Stage 1: Data Platform Foundation

Added project structure, sample job generation, ingestion, skill extraction, database models, SQLAlchemy, Streamlit, FastAPI foundation, and tests.

### Stage 2: ML and Intelligence Layer

Added salary prediction, job category classification, CV matching, skill gap analysis, learning roadmap generation, ML dashboard pages, and ML API endpoints.

### Stage 3: Backend Architecture and System Analyst Layer

Added modular FastAPI routes, Pydantic schemas, service layer, API tests, architecture documentation, data dictionary, model card, and API documentation.

### Stage 4: Full-Stack Frontend

Added Next.js, TypeScript, Tailwind CSS, Recharts, API integration, market page, CV matcher, salary predictor, and skill gap roadmap.

### Stage 5: Data Engineering and MLOps

Added Dockerised backend and frontend, PostgreSQL service, Docker Compose, data quality checks, pipeline script, GitHub Actions CI, MLOps documentation, and deployment guide.

---

## Reports

The project includes system documentation in:

```text
reports/
```

Files:

```text
architecture.md
api_documentation.md
data_dictionary.md
deployment_guide.md
mlops_workflow.md
model_card.md
```

---

## Skills Demonstrated

- Python programming
- Data engineering
- Data ingestion
- Data quality validation
- SQLAlchemy ORM
- PostgreSQL readiness
- SQLite fallback
- Machine learning
- Regression modelling
- Classification modelling
- CV parsing
- Skill extraction
- Recommendation logic
- FastAPI backend development
- Pydantic validation
- API service architecture
- Next.js frontend development
- TypeScript
- Tailwind CSS
- Recharts visualisation
- Docker and Docker Compose
- CI/CD with GitHub Actions
- MLOps workflow design
- System documentation
- Deployment planning

---

## Limitations

- Current job data is synthetic.
- Salary prediction is trained on generated sample data.
- The system is not intended for real hiring decisions.
- The CV matching logic is skill-based and rule-based.
- Real production use would require real job data, privacy safeguards, bias checks, monitoring, and model governance.

---

## Future Improvements

- Real job API ingestion
- Scheduled data pipeline
- Airflow or Prefect orchestration
- dbt transformations
- MLflow experiment tracking
- Vector database for semantic CV matching
- RAG-based career assistant
- User accounts
- Authentication
- Saved CV profiles
- More advanced salary models
- Model monitoring
- Cloud deployment automation
- Kubernetes deployment

---

## Author

**Ameer Hamza**

Data Scientist | Data Analyst

GitHub: https://github.com/ameerhamzarashid  
LinkedIn: https://www.linkedin.com/in/ameerhamza78644

---

## Disclaimer

SkillLens AI is an educational and portfolio project.

It should not be used for automated hiring decisions or employment screening without proper validation, privacy review, fairness testing, and legal compliance.
