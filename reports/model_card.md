
---

# 22. ADD `reports/model_card.md`

```md
# SkillLens AI Model Card

## Overview

SkillLens AI Stage 2 and Stage 3 include two machine learning models:

1. Salary prediction model
2. Job category classification model

These models are trained on the generated sample job dataset.

---

## Model 1: Salary Prediction

### Model Type

Random Forest Regressor

### Target

Salary midpoint:

```text
(salary_min + salary_max) / 2