import requests
import trafilatura
from bs4 import BeautifulSoup
import json
from pathlib import Path
from crewai.tools import tool


def convert_job_page_to_markdown(url: str) -> str:
    """
    Extract a job posting from a webpage and save the result as Markdown.
    """
    markdown_path = "data/job.md"

    try:
        response = requests.get(
            url,
        )
        response.raise_for_status()

        text = trafilatura.extract(
            response.text,
            include_links=False,
            include_images=False,
            include_tables=True,
        )

        if text:
            print("[TOOL] Trafilatura successfully extracted text.")
        else:
            raise ValueError("Trafilatura returned no text.")

    except Exception as error:
        print(f"[TOOL] Trafilatura failed: {error}. " "Falling back to BeautifulSoup.")

        response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup(["script", "style", "noscript"]):
            element.decompose()

        text = soup.get_text("\n", strip=True)

    if not text:
        raise ValueError("Could not extract text from the webpage.")

    print(f"[TOOL] Job posting saved to {markdown_path}")
    print(f"[TOOL] Extracted {len(text)} characters")

    return text


def convert_job_description_to_markdown(description: str) -> str:
    """
    Save a job description as Markdown and return its content.
    """
    print(f"[TOOL] Received {len(description)} characters")

    return description


@tool("convert_job_to_markdown")
def convert_job_to_markdown(job: str) -> str:
    """
    Extract a job posting from a URL or process an existing job description.
    Automatically detects whether the input is a URL or plain text.
    """
    job = job.strip()

    if job.startswith(("http://", "https://")):
        print("[TOOL] Input detected as URL.")
        return convert_job_page_to_markdown(job)

    print("[TOOL] Input detected as job description.")
    return convert_job_description_to_markdown(job)


@tool("save_structured_job")
def save_structured_job(structured_job: str) -> None:
    """
    Save a structured job posting as a formatted JSON file.
    """

    json_path = Path("data/structured_job_temp.json")

    data = json.loads(structured_job)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"[TOOL] Structured job saved to {json_path}")
    print(f"[TOOL] Saved {len(data)} top-level fields")


if __name__ == "__main__":
    job = input("Enter the job posting URL or description: ")
    convert_job_to_markdown.run(job)
