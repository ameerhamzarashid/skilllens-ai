# SkillLens AI MLOps Workflow

## Overview

Stage 5 adds a basic MLOps workflow for SkillLens AI.

The workflow covers:

- Data generation
- Data ingestion
- Data quality checks
- Model training
- Model artefact saving
- Test execution
- CI validation through GitHub Actions

---

## Pipeline Steps

```text
Generate sample jobs
    ↓
Ingest jobs into database
    ↓
Run data quality checks
    ↓
Train salary prediction model
    ↓
Train job category model
    ↓
Run backend and ML tests
    ↓
Save reports and model artefacts