from pathlib import Path

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


