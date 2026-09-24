import json
from pathlib import Path
import yaml

from crewai.tools import tool

FRAMEWORK_PATH = Path("src/config/evaluation_framework.yaml")


@tool("get_evaluation_framework")
def get_evaluation_framework() -> str:
    """
    Load the evaluation framework used by the Reviewer.
    """

    with open(FRAMEWORK_PATH, "r", encoding="utf-8") as file:
        framework = yaml.safe_load(file)

    return yaml.dump(
        framework,
        allow_unicode=True,
        sort_keys=False,
    )


@tool("save_structured_review")
def save_structured_review(structured_review: str) -> None:
    """
    Save a structured review as a formatted JSON file.
    """

    json_path = Path("data/structured_review_temp.json")

    data = json.loads(structured_review)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"[TOOL] Structured Review saved to {json_path}")
