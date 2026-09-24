import json
from pathlib import Path

from crewai.tools import tool


@tool("ask_user")
def ask_user(question: str) -> str:
    """
    Ask the candidate one focused question and return the answer.
    """

    print(f"[OPTIMIZER QUESTION] {question}")
    return input("Answer: ").strip()


@tool("save_structured_optimization")
def save_structured_optimization(structured_optimization: str) -> None:
    """
    Save the structured CV optimization as a formatted JSON file.
    """

    json_path = Path("data/structured_optimization_temp.json")
    data = json.loads(structured_optimization)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"[TOOL] Structured optimization saved to {json_path}")


@tool("save_optimized_cv_markdown")
def save_optimized_cv_markdown(optimized_cv_markdown: str) -> None:
    """
    Save the optimized CV draft as a Markdown file.
    """

    markdown_path = Path("data/optimized_cv.md")
    markdown_path.write_text(optimized_cv_markdown, encoding="utf-8")

    print(f"[TOOL] Optimized CV saved to {markdown_path}")
