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


