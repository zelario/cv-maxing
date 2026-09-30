from pathlib import Path

import pdfplumber
from crewai.tools import tool


@tool("convert_cv_to_markdown")
def convert_cv_to_markdown(pdf_path: str) -> str:
    """
    Extract the text of a CV PDF and return it.

    Use this tool whenever a CV PDF needs to be extracted before parsing.
    """

    print(f"[TOOL] Starting CV conversion: {pdf_path}")

    with pdfplumber.open(Path(pdf_path)) as pdf:
        text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)

    print("[TOOL] CV conversion completed successfully")

    return text