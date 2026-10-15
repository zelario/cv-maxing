import argparse
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pdfplumber

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
TESTS_SRC_DIR = PROJECT_ROOT / "tests" / "src"
TEMP_DIR = PROJECT_ROOT / "temp"

# ==============================================================================
# CONFIGURATION - Set test file paths here (or pass via command-line arguments)
# ==============================================================================
CV_PATH = PROJECT_ROOT / "tests" / "cvs" / "cv.pdf"
JOB_PATH = PROJECT_ROOT / "tests" / "jobs" / "job.md"
PROFILE_PATH = None  # e.g. PROJECT_ROOT / "tests" / "profiles" / "profile_doctor.md"
# ==============================================================================

for path in (PROJECT_ROOT, SRC_DIR, TESTS_SRC_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

load_dotenv(PROJECT_ROOT / ".env")

try:
    from candidate import Candidate
    from crew import CVMaxingCrew
    from judge import Judge
    from tools.cv_generation import render_cv_html, render_cv_pdf
    from tools.cv_optimization import set_question_handler
    from utils.save_outputs import save_pipeline_outputs
except ImportError:
    from tests.src.candidate import Candidate
    from src.crew import CVMaxingCrew
    from tests.src.judge import Judge
    from src.tools.cv_generation import render_cv_html, render_cv_pdf
    from src.tools.cv_optimization import set_question_handler
    from src.utils.save_outputs import save_pipeline_outputs


def run_pipeline(
    cv_path: Path, job_path: Path, profile_path: Path | None, model: str
) -> None:
    """Runs 1 complete test: Candidate -> CVMaxingCrew -> Render PDF -> Judge."""
    print(f"\n{'='*60}")
    print(f"[PIPELINE] Starting Test")
    print(f"  CV:      {cv_path.name}")
    print(f"  Job:     {job_path.name}")
    print(f"  Profile: {profile_path.name if profile_path else 'None (CV only)'}")
    print(f"  Model:   {model}")
    print(f"{'='*60}\n")

    if not cv_path.is_file():
        raise FileNotFoundError(f"CV file not found: {cv_path}")
    if not job_path.is_file():
        raise FileNotFoundError(f"Job file not found: {job_path}")

    # 1. Read input data
    with pdfplumber.open(cv_path) as pdf:
        cv_text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
    job_text = job_path.read_text(encoding="utf-8").strip()
    extra_context = (
        profile_path.read_text(encoding="utf-8").strip()
        if profile_path and profile_path.is_file()
        else ""
    )

    # 2. Prepare candidate simulator
    candidate = Candidate(
        cv_text=cv_text,
        job_text=job_text,
        extra_context=extra_context,
        model=model,
    )
    set_question_handler(candidate.answer_question)

    # 3. Run CrewAI pipeline
    try:
        crew_result = (
            CVMaxingCrew().crew().kickoff(inputs={"cv": str(cv_path), "job": job_text})
        )
        generated_cv = save_pipeline_outputs(crew_result)
        pdf_bytes = render_cv_pdf(render_cv_html(generated_cv))
        (TEMP_DIR / "optimized_cv.pdf").write_bytes(pdf_bytes)
        print("\n[PIPELINE] Optimized CV PDF saved to temp/optimized_cv.pdf")
    finally:
        set_question_handler(None)

    # Save question/answer transcript
    (TEMP_DIR / "simulated_conversation.json").write_text(
        json.dumps(candidate.conversation, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # 4. Evaluate with Judge
    Judge(model=model).evaluate(directory=TEMP_DIR)


def main():
    parser = argparse.ArgumentParser(description="CV Maxing Validation Pipeline")
    parser.add_argument(
        "--cv", type=str, default=str(CV_PATH), help="Path to CV PDF file"
    )
    parser.add_argument(
        "--job", type=str, default=str(JOB_PATH), help="Path to Job file"
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=str(PROFILE_PATH) if PROFILE_PATH else None,
        help="Path to candidate profile file",
    )
    parser.add_argument(
        "--judge-only",
        action="store_true",
        help="Run only the Judge on existing temp/ files",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("JUDGE_MODEL") or os.getenv("MODEL", "gemini-3.5-flash-lite"),
        help="LLM model",
    )
    args = parser.parse_args()

    if args.judge_only:
        Judge(model=args.model).evaluate(directory=TEMP_DIR)
    else:
        cv_path = Path(args.cv)
        job_path = Path(args.job)
        profile_path = Path(args.profile) if args.profile else None
        run_pipeline(
            cv_path=cv_path,
            job_path=job_path,
            profile_path=profile_path,
            model=args.model,
        )


if __name__ == "__main__":
    main()
