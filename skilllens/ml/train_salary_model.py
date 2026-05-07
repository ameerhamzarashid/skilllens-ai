import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from skilllens.ml.model_utils import (
    SALARY_MODEL_PATH,
    SALARY_REPORT_PATH,
    ensure_ml_dirs,
    load_training_jobs,
    salary_midpoint,
    save_json_report,
    save_model,
)


def prepare_salary_training_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepare features and target for salary prediction.
    """
    required = [
        "category",
        "experience_level",
        "work_type",
        "location",
        "salary_min",
        "salary_max",
        "extracted_skills",
    ]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    data = df.dropna(subset=["salary_min", "salary_max"]).copy()

    data["salary_mid"] = salary_midpoint(data)
    data["skill_count"] = data["extracted_skills"].fillna("").apply(
        lambda value: len([x for x in str(value).split(",") if x.strip()])
    )

    x = data[
        [
            "category",
            "experience_level",
            "work_type",
            "location",
            "skill_count",
        ]
    ].copy()

    y = data["salary_mid"]

    return x, y


def train_salary_model() -> dict:
    """
    Train salary prediction model and save artefacts.
    """
    ensure_ml_dirs()

    df = load_training_jobs()

    if df.empty:
        raise ValueError("No job data available. Run ingestion first.")

    x, y = prepare_salary_training_data(df)

    categorical_features = [
        "category",
        "experience_level",
        "work_type",
        "location",
    ]

    numeric_features = ["skill_count"]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
            ("num", "passthrough", numeric_features),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=250,
        random_state=42,
        min_samples_leaf=2,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
    )

    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    save_model(pipeline, SALARY_MODEL_PATH)

    report = {
        "model_name": "RandomForestRegressor",
        "target": "salary_midpoint",
        "rows": int(len(df)),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "mae": round(float(mae), 2),
        "r2_score": round(float(r2), 4),
        "features": [
            "category",
            "experience_level",
            "work_type",
            "location",
            "skill_count",
        ],
        "model_path": str(SALARY_MODEL_PATH),
    }

    save_json_report(report, SALARY_REPORT_PATH)

    return report


def predict_salary(
    category: str,
    experience_level: str,
    work_type: str,
    location: str,
    skill_count: int,
) -> float:
    """
    Predict salary from user inputs.
    """
    from skilllens.ml.model_utils import load_model

    model = load_model(SALARY_MODEL_PATH)

    x = pd.DataFrame(
        [
            {
                "category": category,
                "experience_level": experience_level,
                "work_type": work_type,
                "location": location,
                "skill_count": skill_count,
            }
        ]
    )

    prediction = model.predict(x)[0]

    return round(float(prediction), 2)


if __name__ == "__main__":
    result = train_salary_model()
    print("Salary model training complete.")
    print(result)