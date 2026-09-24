# CV Maxing

AI-powered CV optimization tool that analyzes your CV against a specific job posting and helps you improve it.

## Features

* Parse your CV from PDF
* Parse a job posting from a URL or description
* Get a structured CV and job representation
* Evaluate CV evidence against job requirements
* Identify missing and weak evidence
* Get an AI-powered review
* Get a deterministic CV-job evaluation
* Receive CV improvement suggestions
* Optimize and re-evaluate your CV
* Approve or reject AI suggestions

## How It Works

```text
CV + Job Posting

       ↓

   CV / Job Parsing

       ↓

Structured CV + Job

       ↓

Deterministic Evaluation + AI Review

       ↓

    Improvements

       ↓

  Human Approval

       ↓

  CV Optimization

       ↓

   Re-evaluation
```

## Tech Stack

* Python
* CrewAI
* LLMs
* OpenRouter
* Pydantic
* Docling
* Trafilatura
* BeautifulSoup
* PyYAML
* Sentence Transformers
* Streamlit
* SQLite / PostgreSQL

## Status

In development

## Setup

1. Install Python 3.10 or newer and make sure `python` is available in PowerShell.

2. From the project root, create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

5. Add your API key and model to `.env`.

Example:

```env
OPENROUTER_API_KEY=your_api_key
MODEL=openrouter/openrouter/free
```

6. Run the project:

```powershell
python -m src.main
```
