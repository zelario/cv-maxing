import requests
from bs4 import BeautifulSoup
from crewai.tools import tool


def convert_job_page_to_markdown(url: str) -> str:
    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    text = soup.get_text("\n", strip=True)
    if not text:
        raise ValueError("Could not extract text from the webpage.")

    print(f"[TOOL] Extracted {len(text)} characters")
    return text


def convert_job_description_to_markdown(description: str) -> str:
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


if __name__ == "__main__":
    job = input("Enter the job posting URL or description: ")
    print(convert_job_to_markdown.run(job))