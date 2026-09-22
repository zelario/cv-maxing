import requests
import trafilatura
from bs4 import BeautifulSoup


def parse_job_page(url: str, markdown_path: str = None) -> None:

    if markdown_path is None:
        markdown_path = "data/job.md"

    try:
        response = requests.get(url)
        response.raise_for_status()

        text = trafilatura.extract(
            response.text,
            include_links=False,
            include_images=False,
            include_tables=True
        )
        
        print("Trafilatura successfully extracted text from the webpage.")
        
    except Exception:
        
        print("Trafilatura failed to extract text. Falling back to BeautifulSoup.")
        
        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup(["script", "style", "noscript"]):
            element.decompose()

        text = soup.get_text("\n", strip=True)

    if not text:
        raise ValueError("Could not extract text from the webpage.")

    with open(markdown_path, "w", encoding="utf-8") as file:
        file.write(text)


if __name__ == "__main__":
    parse_job_page(input("Enter the job posting URL: "))