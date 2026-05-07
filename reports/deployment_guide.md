
---

# 13. ADD `reports/deployment_guide.md`

```md
# SkillLens AI Deployment Guide

## Local Development

SkillLens AI can be run locally with:

- FastAPI backend
- Next.js frontend
- SQLite fallback
- Optional PostgreSQL through Docker

---

## Option 1: Local Python and Node

### Terminal 1: Backend

```bash
python -m data_platform.generate_sample_jobs
python -m data_platform.ingest_jobs
python -m skilllens.ml.train_salary_model
python -m skilllens.ml.train_category_model
uvicorn backend.main:app --reload