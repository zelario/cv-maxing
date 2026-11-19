import io
import os
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
import pdfplumber
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
load_dotenv(ROOT / ".env")

from crew import CVMaxingCrew
from models.optimization import CVOptimizationResult
from models.review import ReviewerResult
from tools.cv_generation import render_cv_html, render_cv_pdf
from tools.cv_optimization import set_question_handler
from utils.save_outputs import save_pipeline_outputs

app = FastAPI(title="CV Maxing API")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")

MAX_CV_SIZE = 15 * 1024 * 1024
QUESTION_TIMEOUT_SECONDS = 30 * 60
SESSION_MAX_RETAINED = 30
SESSION_TTL_SECONDS = 7200  # 2 hours

_jobs: dict[str, "Session"] = {}
_jobs_lock = threading.Lock()
_active_job_id: str | None = None


def _clean_expired_sessions() -> None:
    """Evicts completed or errored sessions older than TTL, or keeps dictionary size under SESSION_MAX_RETAINED."""
    now = time.time()
    expired_ids = [
        jid
        for jid, s in _jobs.items()
        if s.status in ("complete", "error")
        and (now - s.last_accessed > SESSION_TTL_SECONDS)
    ]
    for jid in expired_ids:
        _jobs.pop(jid, None)

    # If still exceeding capacity, prune oldest inactive sessions
    if len(_jobs) > SESSION_MAX_RETAINED:
        inactive_jobs = sorted(
            [s for s in _jobs.values() if s.status in ("complete", "error")],
            key=lambda s: s.last_accessed,
        )
        to_remove = len(_jobs) - SESSION_MAX_RETAINED
        for s in inactive_jobs[:to_remove]:
            _jobs.pop(s.job_id, None)


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
        self.stage = "queued"
        self.stage_message = "Preparing analysis..."
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.question_id = 0
        self.question: str | None = None
        self.answer: str | None = None
        self.answer_event: threading.Event | None = None
        self.result: dict | None = None
        self.error: str | None = None
        self.output_pdf_bytes: bytes | None = None

    def set_stage(self, stage: str, message: str) -> None:
        with self.lock:
            self.stage = stage
            self.stage_message = message
            self.last_accessed = time.time()

    def ask(self, question: str) -> str:
        with self.lock:
            self.question_id += 1
            self.question = question.strip()
            self.answer = None
            self.answer_event = threading.Event()
            event = self.answer_event
            self.status = "waiting_question"
            self.stage = "waiting_question"
            self.stage_message = "Awaiting your clarification..."
            self.last_accessed = time.time()

        if not event.wait(QUESTION_TIMEOUT_SECONDS):
            raise TimeoutError("The candidate did not answer within 30 minutes.")

        with self.lock:
            answer = self.answer
            self.status = "processing"
            self.stage = "optimizing"
            self.stage_message = "Integrating your input..."
            self.last_accessed = time.time()
        return answer or ""

    def public_state(self) -> dict:
        with self.lock:
            self.last_accessed = time.time()
            return {
                "id": self.job_id,
                "status": self.status,
                "stage": self.stage,
                "stage_message": self.stage_message,
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
        session.set_stage("parsing", "Extracting and analyzing CV and job requirements...")
        set_question_handler(session.ask)
        result = (
            CVMaxingCrew()
            .crew()
            .kickoff(inputs={"cv": session.pdf_path, "job": session.job_description})
        )
        session.set_stage("generating", "Consolidating final CV schema and formatting content...")
        generated = save_pipeline_outputs(result, job_id=session.job_id)

        session.set_stage("rendering", "Rendering pixel-perfect ATS-compliant PDF...")
        session_pdf_bytes = render_cv_pdf(render_cv_html(generated))

        # Save session-isolated PDF output as well as shared fallback
        pdf_path = ROOT / "temp" / f"optimized_cv_{session.job_id}.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(session_pdf_bytes)

        default_pdf_path = ROOT / "temp" / "optimized_cv.pdf"
        default_pdf_path.write_bytes(session_pdf_bytes)

        task_outputs = getattr(result, "tasks_output", [])
        review_obj = next(
            (
                t.pydantic
                for t in task_outputs
                if isinstance(getattr(t, "pydantic", None), ReviewerResult)
            ),
            (
                task_outputs[2].pydantic
                if len(task_outputs) > 2
                and isinstance(task_outputs[2].pydantic, ReviewerResult)
                else None
            ),
        )
        opt_obj = next(
            (
                t.pydantic
                for t in task_outputs
                if isinstance(getattr(t, "pydantic", None), CVOptimizationResult)
            ),
            (
                task_outputs[3].pydantic
                if len(task_outputs) > 3
                and isinstance(task_outputs[3].pydantic, CVOptimizationResult)
                else None
            ),
        )
        payload = {
            "cv": generated.model_dump(),
            "review": review_obj.model_dump() if review_obj else {},
            "optimization": opt_obj.model_dump() if opt_obj else {},
        }
        with session.lock:
            session.result = payload
            session.output_pdf_bytes = session_pdf_bytes
            session.status = "complete"
            session.stage = "complete"
            session.stage_message = "CV optimization complete!"
            session.last_accessed = time.time()
    except Exception as exc:
        with session.lock:
            session.error = str(exc)
            session.status = "error"
            session.stage = "error"
            session.stage_message = f"Error: {exc}"
            session.last_accessed = time.time()
    finally:
        set_question_handler(None)
        if os.path.exists(session.pdf_path):
            try:
                os.remove(session.pdf_path)
            except OSError:
                pass
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

    # Pre-flight PDF text content validation (Item 4)
    try:
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            if not pdf.pages:
                raise HTTPException(
                    status_code=400,
                    detail="The uploaded PDF contains no pages.",
                )
            extracted_text = "".join(page.extract_text() or "" for page in pdf.pages)
            if len(extracted_text.strip()) < 50:
                raise HTTPException(
                    status_code=400,
                    detail="The PDF contains insufficient readable text (scanned image or empty). Please upload a text-based PDF CV.",
                )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read or parse PDF: {exc}",
        )

    with _jobs_lock:
        _clean_expired_sessions()
        if _active_job_id is not None:
            raise HTTPException(
                status_code=409,
                detail="An optimization is already running. Try again later.",
            )
        job_id = uuid.uuid4().hex
        with tempfile.NamedTemporaryFile(
            prefix="cv-maxing-original-",
            suffix=".pdf",
            delete=False,
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


@app.get("/api/jobs/{job_id}/pdf")
async def download_job_pdf(job_id: str):
    with _jobs_lock:
        session = _jobs.get(job_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Optimization not found.")

    with session.lock:
        session.last_accessed = time.time()
        if session.status != "complete" or session.output_pdf_bytes is None:
            # Fallback check on isolated disk PDF
            isolated_pdf = ROOT / "temp" / f"optimized_cv_{session.job_id}.pdf"
            if isolated_pdf.exists():
                session.output_pdf_bytes = isolated_pdf.read_bytes()
            else:
                raise HTTPException(status_code=409, detail="The CV PDF is not ready.")
        pdf_bytes = session.output_pdf_bytes

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'inline; filename="optimized-cv.pdf"'},
    )


@app.post("/api/jobs/{job_id}/answer")
async def answer_question(job_id: str, body: Question):
    with _jobs_lock:
        session = _jobs.get(job_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Optimization not found.")

    with session.lock:
        session.last_accessed = time.time()
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
        session.stage = "optimizing"
        session.stage_message = "Processing your response..."
        event = session.answer_event
        if event is None:
            raise HTTPException(status_code=409, detail="There is no pending question.")
        event.set()
    return {"status": "processing"}
