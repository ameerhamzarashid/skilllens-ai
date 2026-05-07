
---

# 21. ADD `reports/data_dictionary.md`

```md
# SkillLens AI Data Dictionary

## Table: job_postings

This table stores cleaned job posting records.

| Column | Type | Description |
|---|---|---|
| id | integer | Internal primary key |
| job_id | string | Unique job identifier |
| title | string | Job title |
| company | string | Hiring company |
| location | string | Job location |
| country | string | Country |
| category | string | Normalised job category |
| experience_level | string | Entry Level, Junior, Mid Level or Senior |
| work_type | string | Remote, Hybrid or Onsite |
| salary_min | float | Minimum advertised salary |
| salary_max | float | Maximum advertised salary |
| salary_currency | string | Salary currency |
| description | text | Job description |
| extracted_skills | text | Comma-separated extracted technical skills |
| posted_date | string | Date job was posted |
| source | string | Source of the job record |
| created_at | datetime | Database insertion timestamp |

---

## Generated Dataset

The generated sample dataset is stored at:

```text
data/raw/sample_jobs.csv