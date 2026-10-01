import os
import sys
import tempfile
import threading
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
load_dotenv(ROOT / ".env")

from crew import CVMaxingCrew
from tools.cv_generation import render_cv
from tools.cv_optimization import set_question_handler
from utils.save_outputs import save_pipeline_outputs

app = FastAPI(title="CV Maxing API")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")
MAX_CV_SIZE = 15 * 1024 * 1024
QUESTION_TIMEOUT_SECONDS = 30 * 60

_jobs: dict[str, "Session"] = {}
_jobs_lock = threading.Lock()
_active_job_id: str | None = None


class Question(BaseModel):
    question_id: int
    answer: str


class Session:

    def __init__(self, job_id: str, pdf_path: str, job_description: str):
        self.job_id = job_id
        self.pdf_path = pdf_path
        self.job_description = job_description
        self.lock = threading.Lock()
        self.status = "processing"
        self.question_id = 0
        self.question: str | None = None
        self.answer: str | None = None
        self.answer_event: threading.Event | None = None
        self.result: dict | None = None
        self.error: str | None = None

    def ask(self, question: str) -> str:
        with self.lock:
            self.question_id += 1
            self.question = question.strip()
            self.answer = None
            self.answer_event = threading.Event()
            event = self.answer_event
            self.status = "waiting_question"

        if not event.wait(QUESTION_TIMEOUT_SECONDS):
            raise TimeoutError("The candidate did not answer within 30 minutes.")

        with self.lock:
            answer = self.answer
            self.status = "processing"
        return answer or ""

    def public_state(self) -> dict:
        with self.lock:
            return {
                "id": self.job_id,
                "status": self.status,
                "question_id": (
                    self.question_id if self.status == "waiting_question" else None
                ),
                "question": (
                    self.question if self.status == "waiting_question" else None
                ),
                "result": self.result if self.status == "complete" else None,
                "error": self.error if self.status == "error" else None,
            }


def _run_pipeline(session: Session) -> None:
    global _active_job_id
    try:
        set_question_handler(session.ask)
        result = (
            CVMaxingCrew()
            .crew()
            .kickoff(inputs={"cv": session.pdf_path, "job": session.job_description})
        )
        generated = save_pipeline_outputs(result)
        payload = {
            "markdown": render_cv(generated),
            "cv": generated.model_dump(),
            "review": result.tasks_output[2].pydantic.model_dump(),
            "optimization": result.tasks_output[3].pydantic.model_dump(),
        }
        with session.lock:
            session.result = payload
            session.status = "complete"
    except Exception as exc:
        with session.lock:
            session.error = str(exc)
            session.status = "error"
    finally:
        set_question_handler(None)
        if os.path.exists(session.pdf_path):
            os.remove(session.pdf_path)
        with _jobs_lock:
            if _active_job_id == session.job_id:
                _active_job_id = None


@app.get("/")
async def frontend():
    return FileResponse(ROOT / "frontend" / "index.html")


@app.post("/api/jobs", status_code=202)
async def start_optimization(cv: UploadFile = File(...), job: str = Form(...)):
    global _active_job_id
    if not (cv.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Your CV must be a PDF file.")
    if not job.strip():
        raise HTTPException(status_code=400, detail="Enter the job description.")

    data = await cv.read(MAX_CV_SIZE + 1)
    if len(data) > MAX_CV_SIZE:
        raise HTTPException(status_code=413, detail="The PDF exceeds the 15 MB limit.")
    if not data.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file does not appear to be a valid PDF.",
        )

    with _jobs_lock:
        if _active_job_id is not None:
            raise HTTPException(
                status_code=409,
                detail="An optimization is already running. Try again later.",
            )
        job_id = uuid.uuid4().hex
        temp_dir = ROOT / "temp"
        temp_dir.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile(
            dir=temp_dir, suffix=".pdf", delete=False
        ) as file:
            file.write(data)
            pdf_path = file.name
        session = Session(job_id, pdf_path, job.strip())
        _jobs[job_id] = session
        _active_job_id = job_id

    threading.Thread(target=_run_pipeline, args=(session,), daemon=True).start()
    return {"id": job_id, "status": "processing"}


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    with _jobs_lock:
        session = _jobs.get(job_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Optimization not found.")
    return session.public_state()


@app.post("/api/jobs/{job_id}/answer")
async def answer_question(job_id: str, body: Question):
    with _jobs_lock:
        session = _jobs.get(job_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Optimization not found.")

    with session.lock:
        if (
            session.status != "waiting_question"
            or session.question_id != body.question_id
        ):
            raise HTTPException(
                status_code=409,
                detail="This question was already answered or has expired.",
            )
        if not body.answer.strip():
            raise HTTPException(
                status_code=400, detail="Enter an answer or choose Skip."
            )
        session.answer = body.answer.strip()
        session.status = "processing"
        event = session.answer_event
        if event is None:
            raise HTTPException(status_code=409, detail="There is no pending question.")
        event.set()
    return {"status": "processing"}
