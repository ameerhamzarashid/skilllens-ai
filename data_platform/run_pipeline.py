import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from skilllens.config import ML_REPORT_DIR


PIPELINE_REPORT_PATH = ML_REPORT_DIR / "pipeline_run_report.json"


COMMANDS = [
    {
        "name": "Generate sample jobs",
        "command": [sys.executable, "-m", "data_platform.generate_sample_jobs"],
    },
    {
        "name": "Ingest jobs",
        "command": [sys.executable, "-m", "data_platform.ingest_jobs"],
    },
    {
        "name": "Run data quality checks",
        "command": [sys.executable, "-m", "data_platform.data_quality"],
    },
    {
        "name": "Train salary model",
        "command": [sys.executable, "-m", "skilllens.ml.train_salary_model"],
    },
    {
        "name": "Train category model",
        "command": [sys.executable, "-m", "skilllens.ml.train_category_model"],
    },
    {
        "name": "Run tests",
        "command": [sys.executable, "-m", "pytest"],
    },
]


def run_command(step: dict) -> dict:
    """
    Run one pipeline command and capture result.
    """
    print(f"\nRunning step: {step['name']}")
    print("Command:", " ".join(step["command"]))

    result = subprocess.run(
        step["command"],
        capture_output=True,
        text=True,
    )

    passed = result.returncode == 0

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    return {
        "name": step["name"],
        "command": " ".join(step["command"]),
        "passed": passed,
        "return_code": result.returncode,
        "stdout_tail": result.stdout[-1000:],
        "stderr_tail": result.stderr[-1000:],
    }


def run_pipeline() -> dict:
    """
    Run Stage 5 data and ML pipeline.
    """
    ML_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    started_at = datetime.utcnow().isoformat()

    step_results = []

    for step in COMMANDS:
        result = run_command(step)
        step_results.append(result)

        if not result["passed"]:
            break

    finished_at = datetime.utcnow().isoformat()
    overall_passed = all(step["passed"] for step in step_results)

    report = {
        "pipeline": "SkillLens AI Stage 5 pipeline",
        "started_at": started_at,
        "finished_at": finished_at,
        "overall_passed": overall_passed,
        "steps": step_results,
    }

    PIPELINE_REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    return report


def main():
    report = run_pipeline()

    print("\nPipeline summary:")
    print(json.dumps(report, indent=2))

    if not report["overall_passed"]:
        raise SystemExit("Pipeline failed.")


if __name__ == "__main__":
    main()