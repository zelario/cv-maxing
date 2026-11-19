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

    if len(text.strip()) < 50:
        raise ValueError(
            "Extracted CV text contains fewer than 50 characters. "
            "The PDF may be an un-OCRed scanned image or empty. Please provide a text-based PDF."
        )

    print(f"[TOOL] CV conversion completed successfully ({len(text)} characters extracted)")

    return text