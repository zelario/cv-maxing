from crewai.tools import tool


TEMPLATE_PATH = "src/config/cv_template.md"


@tool("get_cv_template")
def get_cv_template() -> str:
    """Load the Markdown template used to generate the final CV."""

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        return file.read()

