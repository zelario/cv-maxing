# CV Maxing

AI-powered CV optimization tool that analyzes your CV against a specific job posting and helps you improve it.

## Features

* Upload your CV
* Add a job posting
* Get a CV-job fit score
* Identify missing requirements
* Find weak evidence
* Get an AI-powered review
* Receive CV improvement suggestions
* Optimize and re-evaluate your CV
* Approve or reject AI suggestions

## How It Works

```text
CV + Job Posting
       ↓
    AI Review
       ↓
 Match + Score + Reasoning
       ↓
  Improvements
       ↓
 Human Approval
       ↓
   CV Optimization
```

## Tech Stack

* Python
* CrewAI
* LLMs
* Sentence Transformers
* PyMuPDF
* spaCy
* Pydantic
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

4. Create `.env` from `.env.example` and add your Gemini API key:

```powershell
Copy-Item .env.example .env
```

5. Run the crew as a Python module:

```powershell
python -m src.main
```

The current crew contains the CV parser task. Input handling and the remaining agents will be added as the project progresses.
