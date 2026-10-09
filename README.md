# CV Maxing

CV Maxing is a human-centered AI project that helps candidates tailor their CV to a job opportunity. It reviews the information in a CV against a job description, invites the candidate to provide additional context, and generates an updated CV for them to review.

## How it works

1. The candidate provides a CV in PDF format and a job description or link.
2. AI agents extract and structure information from both documents.
3. The system reviews how the CV's evidence relates to the role.
4. The candidate can answer questions or skip them.
5. The system generates an updated CV, available as a PDF or Markdown file.

The candidate remains involved in the process and can review the generated CV before using it.

## Technologies

- **Python** — application logic and AI workflow.
- **CrewAI** — coordination of AI agents and tasks.
- **Large language models (LLMs)** — CV and job analysis, review, and generation.
- **OpenRouter** — access to language models.
- **Pydantic** — structured data models for CVs, job descriptions, and reviews.
- **FastAPI** — backend API.
- **HTML, CSS, and JavaScript** — web interface.
- **Docling, pdfplumber, and Beautiful Soup** — document and job posting extraction.
- **Jinja2 and Playwright** — CV formatting and PDF generation.
- **Docker** — packaging and deployment.

## Project layout

```text
src/
  api.py                 FastAPI app and asynchronous job/session handling
  crew.py                CrewAI agents and pipeline tasks
  config/                Agent and task prompts
  models/                Pydantic data models
  tools/                 CV/job extraction, evaluation, optimization, rendering
  utils/                 Pipeline output helpers
frontend/                Browser interface (HTML, CSS, JavaScript)
docs/                    Project documentation and research notes
tests/                   Sample job description and space for CV inputs
temp/                    Temporary uploads and generated outputs
```

## License

No license has been added to this repository yet.

