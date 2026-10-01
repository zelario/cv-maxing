import requests
from bs4 import BeautifulSoup
from crewai.tools import tool
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def convert_job_page_to_markdown(url: str) -> str:
    retry = Retry(
        total=3,
        connect=3,
        read=2,
        status=3,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.mount("http://", HTTPAdapter(max_retries=retry))

    response = session.get(
        url,
        timeout=(10, 45),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    text = soup.get_text("\n", strip=True)
    if len(text) < 200:
        raise ValueError(
            "Could not extract enough job posting text. Retry later or provide "
            "the job description as text instead of a URL."
        )

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
