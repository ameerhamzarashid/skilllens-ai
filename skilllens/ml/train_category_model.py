import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from skilllens.ml.model_utils import (
    CATEGORY_MODEL_PATH,
    CATEGORY_REPORT_PATH,
    ensure_ml_dirs,
    load_training_jobs,
    save_json_report,
    save_model,
)


def prepare_category_training_data(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """
    Prepare text and labels for job category classification.
    """
    required = ["title", "description", "category"]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    data = df.dropna(subset=["title", "description", "category"]).copy()

    x = data["title"].astype(str) + " " + data["description"].astype(str)
    y = data["category"].astype(str)

    return x, y


def train_category_model() -> dict:
    """
    Train job category classifier.
    """
    ensure_ml_dirs()

    df = load_training_jobs()

    if df.empty:
        raise ValueError("No job data available. Run ingestion first.")

    x, y = prepare_category_training_data(df)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=4000,
                    ngram_range=(1, 2),
                    stop_words="english",
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    detailed_report = classification_report(
        y_test,
        predictions,
        output_dict=True,
        zero_division=0,
    )

    save_model(pipeline, CATEGORY_MODEL_PATH)

    report = {
        "model_name": "TFIDF + LogisticRegression",
        "target": "job_category",
        "rows": int(len(df)),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "accuracy": round(float(accuracy), 4),
        "classification_report": detailed_report,
        "model_path": str(CATEGORY_MODEL_PATH),
    }

    save_json_report(report, CATEGORY_REPORT_PATH)

    return report


def predict_category(text: str) -> str:
    """
    Predict job category from text.
    """
    from skilllens.ml.model_utils import load_model

    model = load_model(CATEGORY_MODEL_PATH)

    prediction = model.predict([text])[0]

    return str(prediction)


if __name__ == "__main__":
    result = train_category_model()
    print("Category model training complete.")
    print(result)