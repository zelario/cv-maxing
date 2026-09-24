from pathlib import Path

from crewai.tools import tool


@tool("ask_user")
def ask_user(question: str) -> str:
    """
    Ask the candidate one focused question and return the answer.
    """

    print(f"[OPTIMIZER QUESTION] {question}")
    return input("Answer: ").strip()


@tool("save_optimized_cv_markdown")
def save_optimized_cv_markdown(optimized_cv_markdown: str) -> None:
    """
    Save the optimized CV draft as a Markdown file.
    """

    markdown_path = Path("temp/optimized_cv.md")
    markdown_path.write_text(optimized_cv_markdown, encoding="utf-8")

    print(f"[TOOL] Optimized CV saved to {markdown_path}")
