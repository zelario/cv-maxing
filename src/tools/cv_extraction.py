from pathlib import Path
import json

from docling.document_converter import DocumentConverter
from crewai.tools import tool


@tool("convert_cv_to_markdown")
def convert_cv_to_markdown(pdf_path: str) -> str:
    """
    Convert a CV PDF into Markdown using Docling and save the result
    next to the original PDF.

    Use this tool whenever a CV PDF needs to be extracted before parsing.
    """

    print(f"[TOOL] Starting CV conversion: {pdf_path}")

    pdf_path = Path(pdf_path)

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    markdown = result.document.export_to_markdown()

    print("[TOOL] CV conversion completed successfully")

    return markdown


@tool("save_structured_cv")
def save_structured_cv(structured_cv: str) -> None:
    """
    Save a structured CV as a formatted JSON file.
    """

    json_path = Path("logs/structured_cv_temp.json")

    data = json.loads(structured_cv)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"[TOOL] Structured CV saved to {json_path}")
    print(f"[TOOL] Saved {len(data)} top-level fields")