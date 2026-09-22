from docling.document_converter import DocumentConverter


def convert_cv_to_markdown(pdf_path: str, markdown_path: str) -> None:
	converter = DocumentConverter()
	result = converter.convert(pdf_path)
	markdown = result.document.export_to_markdown()

	with open(markdown_path, "w", encoding="utf-8") as file:
		file.write(markdown)


if __name__ == "__main__":
	convert_cv_to_markdown("tests/cv.pdf", "tests/cv.md")
