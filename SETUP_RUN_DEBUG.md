# SkillLens AI Setup, Run and Debug Guide

This file explains how to set up, run, test, debug and deploy SkillLens AI.

---

## 1. Project Location

Recommended local path:

```powershell
C:\MyDrive\skilllens-ai
```

Move into the project:

```powershell
cd C:\MyDrive\skilllens-ai
```

---

## 2. Python Virtual Environment

Create virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

You should see:

```text
(.venv) PS C:\MyDrive\skilllens-ai>
```

Deactivate when needed:

```powershell
deactivate
```

---

## 3. Install Python Dependencies

From the root folder:

```powershell
pip install -r requirements.txt
```

If packages fail, upgrade pip:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Database Setup Options

### Option A: SQLite Local Mode

This is easiest for local development.

Make sure `.env` does not exist:

```powershell
del .env
```

If `.env` does not exist, ignore the error.

The app will use:

```text
skilllens_stage1.db
```

### Option B: PostgreSQL Docker Mode

Start PostgreSQL:

```powershell
docker compose up -d postgres
```

Create `.env`:

```powershell
copy .env.example .env
```

Check Docker containers:

```powershell
docker ps
```

---

## 5. Generate Sample Data

From the root folder:

```powershell
python -m data_platform.generate_sample_jobs
```

Expected output:

```text
Sample job dataset created at: C:\MyDrive\skilllens-ai\data\raw\sample_jobs.csv
Rows: 350
```

---

## 6. Ingest Jobs into Database

```powershell
python -m data_platform.ingest_jobs
```

Expected output:

```text
SkillLens AI Stage 1 ingestion complete.
Rows in raw file: 350
Rows inserted: 350
```

If rows inserted is `0`, it usually means the same job IDs already exist in the database.

---

## 7. Run Data Quality Checks

```powershell
python -m data_platform.data_quality
```

Expected:

```text
"overall_passed": true
```

If it fails, regenerate and ingest data:

```powershell
python -m data_platform.generate_sample_jobs
python -m data_platform.ingest_jobs
python -m data_platform.data_quality
```

---

## 8. Train ML Models

Train salary model:

```powershell
python -m skilllens.ml.train_salary_model
```

Train category model:

```powershell
python -m skilllens.ml.train_category_model
```

Expected model files:

```text
ml/models/salary_model.joblib
ml/models/category_model.joblib
```

Expected reports:

```text
ml/reports/salary_model_report.json
ml/reports/category_model_report.json
```

---

## 9. Run Full Data and ML Pipeline

Instead of running each command manually:

```powershell
python -m data_platform.run_pipeline
```

This runs:

```text
Generate sample jobs
Ingest jobs
Run data quality checks
Train salary model
Train category model
Run tests
```

---

## 10. Run FastAPI Backend

From the root folder:

```powershell
uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

## 11. Run Streamlit Dashboard

Open a new terminal.

Activate venv:

```powershell
cd C:\MyDrive\skilllens-ai
.venv\Scripts\activate
```

Run:

```powershell
streamlit run dashboards/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

## 12. Run Next.js Frontend

Open another terminal:

```powershell
cd C:\MyDrive\skilllens-ai\frontend
```

Install frontend dependencies:

```powershell
npm install
```

Create local frontend environment file:

```powershell
copy .env.local.example .env.local
```

Run frontend:

```powershell
npm run dev
```

Open:

```text
http://localhost:3000
```

FastAPI backend must be running at:

```text
http://127.0.0.1:8000
```

---

## 13. Full Local Run Order

Use this order when running manually.

### Terminal 1: Backend

```powershell
cd C:\MyDrive\skilllens-ai
.venv\Scripts\activate
python -m data_platform.run_pipeline
uvicorn backend.main:app --reload
```

### Terminal 2: Frontend

```powershell
cd C:\MyDrive\skilllens-ai\frontend
npm run dev
```

### Optional Terminal 3: Streamlit

```powershell
cd C:\MyDrive\skilllens-ai
.venv\Scripts\activate
streamlit run dashboards/streamlit_app.py
```

---

## 14. Run Tests

From root:

```powershell
python -m pytest
```

Run one test file:

```powershell
python -m pytest tests/test_skill_extractor.py
```

Run API tests:

```powershell
python -m pytest tests/test_api_health.py
python -m pytest tests/test_api_cv.py
```

---

## 15. Build Frontend

From frontend folder:

```powershell
cd C:\MyDrive\skilllens-ai\frontend
npm run build
```

If successful, run production build:

```powershell
npm start
```

Open:

```text
http://localhost:3000
```

---

## 16. Run Full Stack with Docker

Make sure Docker Desktop is running.

From project root:

```powershell
cd C:\MyDrive\skilllens-ai
docker compose up --build
```

Open:

```text
Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

Stop Docker:

```powershell
docker compose down
```

Stop Docker and remove database volume:

```powershell
docker compose down -v
```

---

## 17. Git Workflow

Check status:

```powershell
git status
```

Add all changes:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Update SkillLens AI"
```

Push:

```powershell
git push
```

Full workflow:

```powershell
git status
git add .
git commit -m "Update SkillLens AI"
git push
```

---

# Debug Guide

---

## Issue 1: Repository Not Found During Clone

Error:

```text
Repository not found.
```

Cause:

The GitHub repository does not exist yet, or the URL is wrong.

Fix:

Create the repository on GitHub first, then push local project:

```powershell
git init
git branch -M main
git remote add origin https://github.com/ameerhamzarashid/skilllens-ai.git
git push -u origin main
```

If remote exists:

```powershell
git remote set-url origin https://github.com/ameerhamzarashid/skilllens-ai.git
git push -u origin main
```

---

## Issue 2: Cannot Find Path `skilllens-ai\skilllens-ai`

Error:

```text
Cannot find path 'C:\MyDrive\skilllens-ai\skilllens-ai'
```

Cause:

You are already inside the project folder.

Fix:

Do not run:

```powershell
cd skilllens-ai
```

Stay here:

```powershell
C:\MyDrive\skilllens-ai
```

---

## Issue 3: PostgreSQL Connection Refused

Error:

```text
connection to server at "localhost", port 5432 failed: Connection refused
```

Cause:

`.env` exists and points to PostgreSQL, but PostgreSQL is not running.

Fix option A, use SQLite:

```powershell
del .env
python -m data_platform.ingest_jobs
```

Fix option B, start PostgreSQL:

```powershell
docker compose up -d postgres
python -m data_platform.ingest_jobs
```

---

## Issue 4: `ModuleNotFoundError: No module named 'skilllens'`

Cause:

Python cannot detect the project root.

Fix:

Run commands from the project root:

```powershell
cd C:\MyDrive\skilllens-ai
```

Use module commands:

```powershell
python -m data_platform.generate_sample_jobs
python -m data_platform.ingest_jobs
```

Do not run Python files by double-clicking.

---

## Issue 5: Streamlit App Cannot Load Data

Error:

```text
No data found.
```

Fix:

```powershell
python -m data_platform.generate_sample_jobs
python -m data_platform.ingest_jobs
streamlit run dashboards/streamlit_app.py
```

---

## Issue 6: Salary Predictor Says Model Not Found

Cause:

Salary model has not been trained.

Fix:

```powershell
python -m skilllens.ml.train_salary_model
```

Also train category model:

```powershell
python -m skilllens.ml.train_category_model
```

---

## Issue 7: Frontend Cannot Connect to Backend

Symptoms:

```text
Backend connection error
Failed to fetch
```

Fix:

Start FastAPI backend:

```powershell
cd C:\MyDrive\skilllens-ai
.venv\Scripts\activate
uvicorn backend.main:app --reload
```

Check:

```text
http://127.0.0.1:8000/docs
```

Check `frontend/.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

Restart frontend:

```powershell
cd frontend
npm run dev
```

---

## Issue 8: `npm` Not Recognised

Error:

```text
npm is not recognized
```

Cause:

Node.js is not installed.

Fix:

Install Node.js LTS, then reopen PowerShell and check:

```powershell
node -v
npm -v
```

---

## Issue 9: Frontend Build Fails

Run:

```powershell
cd C:\MyDrive\skilllens-ai\frontend
npm install
npm run build
```

If dependency issue persists:

```powershell
rmdir /s /q node_modules
del package-lock.json
npm install
npm run build
```

---

## Issue 10: Docker Build Fails

First check Docker:

```powershell
docker version
docker compose version
```

Make sure Docker Desktop is open.

Then run:

```powershell
docker compose down
docker compose up --build
```

If database volume is corrupted:

```powershell
docker compose down -v
docker compose up --build
```

---

## Issue 11: Port Already in Use

### FastAPI port 8000 already in use

Run backend on a different port:

```powershell
uvicorn backend.main:app --reload --port 8001
```

Then update frontend `.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001
```

### Next.js port 3000 already in use

Run:

```powershell
npm run dev -- -p 3001
```

Open:

```text
http://localhost:3001
```

### Streamlit port 8501 already in use

Run:

```powershell
streamlit run dashboards/streamlit_app.py --server.port 8502
```

---

## Issue 12: Pytest Fails Because Model Files Are Missing

Run pipeline first:

```powershell
python -m data_platform.run_pipeline
```

Then:

```powershell
python -m pytest
```

---

## Issue 13: Git Says Nothing to Commit

Message:

```text
nothing to commit, working tree clean
```

Meaning:

Everything is already committed.

Push anyway:

```powershell
git push
```

---

## Issue 14: Git Remote Already Exists

Error:

```text
remote origin already exists
```

Fix:

```powershell
git remote set-url origin https://github.com/ameerhamzarashid/skilllens-ai.git
git push -u origin main
```

---

# Deployment Guide

---

## Recommended Deployment

Use:

```text
Frontend: Vercel
Backend: Render
Database: Neon PostgreSQL
```

---

## Step 1: Deploy Database on Neon

Create a Neon PostgreSQL database.

Copy the connection string.

Convert:

```env
postgresql://username:password@host/dbname?sslmode=require
```

To:

```env
postgresql+psycopg2://username:password@host/dbname?sslmode=require
```

---

## Step 2: Deploy Backend on Render

Create Render Web Service from GitHub repository.

Settings:

```text
Root Directory: leave empty
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Environment variables:

```env
APP_NAME=SkillLens AI
APP_ENV=production
DATABASE_URL=postgresql+psycopg2://YOUR_NEON_DATABASE_URL
```

For first backend deployment, use this temporary start command:

```bash
python -m data_platform.generate_sample_jobs && python -m data_platform.ingest_jobs && python -m skilllens.ml.train_salary_model && python -m skilllens.ml.train_category_model && uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

After first successful deploy, change start command back to:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Check backend:

```text
https://your-render-backend-url.onrender.com/docs
```

---

## Step 3: Deploy Frontend on Vercel

Import GitHub repository.

Settings:

```text
Root Directory: frontend
Framework: Next.js
Install Command: npm install
Build Command: npm run build
Output Directory: .next
```

Environment variable:

```env
NEXT_PUBLIC_API_BASE_URL=https://your-render-backend-url.onrender.com
```

Deploy.

Check frontend:

```text
https://your-vercel-app-url.vercel.app
```

---

## Step 4: Test Live Deployment

Test frontend pages:

```text
/
/market
/cv-match
/salary
/skill-gap
```

Test backend:

```text
/health
/jobs/summary
/skills/top
/cv/match-jobs
/ml/predict-salary
```

---

## Step 5: Add Live Links to README

Add:

```md
## Live Deployment

Frontend:
https://your-vercel-app-url.vercel.app

Backend API:
https://your-render-backend-url.onrender.com/docs

Database:
Neon PostgreSQL
```

Commit:

```powershell
git status
git add README.md
git commit -m "Add live deployment links"
git push
```

---

# Useful Command Summary

## Full local backend setup

```powershell
cd C:\MyDrive\skilllens-ai
.venv\Scripts\activate
python -m data_platform.run_pipeline
uvicorn backend.main:app --reload
```

## Full local frontend setup

```powershell
cd C:\MyDrive\skilllens-ai\frontend
npm install
npm run dev
```

## Streamlit dashboard

```powershell
cd C:\MyDrive\skilllens-ai
.venv\Scripts\activate
streamlit run dashboards/streamlit_app.py
```

## Docker full stack

```powershell
cd C:\MyDrive\skilllens-ai
docker compose up --build
```

## Tests

```powershell
python -m pytest
```

## Frontend build

```powershell
cd frontend
npm run build
```

## Git push

```powershell
git status
git add .
git commit -m "Update SkillLens AI"
git push
```
