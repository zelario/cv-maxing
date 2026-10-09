import os
import sys
import json
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR))

from dotenv import load_dotenv
from judge import Judge

PROJECT_ROOT = _THIS_DIR.parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "temp"

def _load_json(filename: str) -> dict:
    path = DATA_DIRECTORY / filename
    if not path.is_file():
        raise FileNotFoundError(f"Required pipeline output was not found: {path}")
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def run():
    filenames = (
        "temp_cv.json",
        "temp_job.json",
        "temp_review.json",
        "temp_optimization.json",
        "temp_generated_cv.json",
    )
    pipeline_outputs = [(filename, _load_json(filename)) for filename in filenames]

    load_dotenv()
    judge_model = os.getenv("JUDGE_MODEL") or os.getenv(
        "MODEL", "gemini-3.5-flash-lite"
    )
    validation = Judge(model=judge_model).evaluate(
        pipeline_outputs=pipeline_outputs,
    )
    output_path = DATA_DIRECTORY / "temp_judge.json"
    output_path.write_text(
        validation.model_dump_json(indent=2) + "\n", encoding="utf-8"
    )

    print(f"Judge analysis completed and saved to {output_path}.")


if __name__ == "__main__":
    run()
