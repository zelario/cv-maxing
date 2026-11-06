import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from dotenv import load_dotenv
import pdfplumber

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
TESTS_SRC_DIR = PROJECT_ROOT / "tests" / "src"
RESULTS_DIR = PROJECT_ROOT / "tests" / "results"
TEMP_DIR = PROJECT_ROOT / "temp"

# ==============================================================================
# OFFICIAL TEST MATRIX (T01 - T30)
# ==============================================================================
TEST_CASES: dict[str, tuple[str, str]] = {
    "T01": ("tomas_junior", "data_scientist_intern"),
    "T02": ("tomas_junior", "backend_engineer_mid"),
    "T03": ("tomas_junior", "devops_engineer_mid"),
    "T04": ("diogo_backend", "backend_engineer_mid"),
    "T05": ("diogo_backend", "fullstack_developer_mid"),
    "T06": ("diogo_backend", "devops_engineer_mid"),
    "T07": ("mariana_frontend", "fullstack_developer_mid"),
    "T08": ("mariana_frontend", "data_scientist_intern"),
    "T09": ("pedro_transition", "data_scientist_intern"),
    "T10": ("pedro_transition", "fullstack_developer_mid"),
    "T11": ("goncalo_doctor", "doctor_junior"),
    "T12": ("ines_nurse", "nurse_mid"),
    "T13": ("ines_nurse", "doctor_junior"),
    "T14": ("beatriz_lawyer", "lawyer_junior"),
    "T15": ("tiago_marketing", "marketing_specialist_mid"),
    "T16": ("tiago_marketing", "lawyer_junior"),
    "T17": ("goncalo_doctor", "marketing_specialist_mid"),
    "T18": ("beatriz_lawyer", "backend_engineer_mid"),
    "T19": ("diogo_backend", "lawyer_junior"),
    "T20": ("goncalo_doctor", "data_scientist_intern"),
    "T21": ("rita_lead", "tech_lead_senior"),
    "T22": ("andre_designer", "product_designer_mid"),
    "T23": ("rita_lead", "backend_engineer_mid"),
    "T24": ("diogo_backend", "tech_lead_senior"),
    "T25": ("mariana_frontend", "product_designer_mid"),
    "T26": ("andre_designer", "fullstack_developer_mid"),
    "T27": ("pedro_transition", "tech_lead_senior"),
    "T28": ("tomas_junior", "product_designer_mid"),
    "T29": ("tiago_marketing", "product_designer_mid"),
    "T30": ("rita_lead", "devops_engineer_mid"),
}
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
    cv_path: Path,
    job_path: Path,
    profile_path: Path | None,
    model: str,
    output_dir: Path | None = None,
) -> None:
    """Runs 1 complete test: Candidate -> CVMaxingCrew -> Render PDF -> Judge."""
    print(f"\n{'='*60}")
    print(f"[PIPELINE] Starting Test")
    print(f"  CV:         {cv_path.name}")
    print(f"  Job:        {job_path.name}")
    print(f"  Profile:    {profile_path.name if profile_path else 'None (CV only)'}")
    print(f"  Model:      {model}")
    if output_dir:
        print(f"  Output Dir: {output_dir}")
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
    candidate_model = os.getenv("MODEL_CANDIDATE") or os.getenv("CANDIDATE_MODEL") or model
    candidate = Candidate(
        cv_text=cv_text,
        job_text=job_text,
        extra_context=extra_context,
        model=candidate_model,
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
    judge_model = os.getenv("MODEL_JUDGE") or os.getenv("JUDGE_MODEL") or model
    Judge(model=judge_model).evaluate(directory=TEMP_DIR)

    # 5. Archive outputs to designated test directory if requested
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        result_files = [
            "temp_cv.json",
            "temp_job.json",
            "temp_review.json",
            "temp_optimization.json",
            "temp_generated_cv.json",
            "temp_judge.json",
            "simulated_conversation.json",
            "optimized_cv.pdf",
        ]
        for fname in result_files:
            src = TEMP_DIR / fname
            if src.is_file():
                shutil.copy2(src, output_dir / fname)
        print(f"\n[PIPELINE] All test outputs archived to {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="CV Maxing Validation Pipeline")
    parser.add_argument(
        "--test-id",
        type=str,
        default=None,
        help="Test ID from matrix (e.g. T01, T02, ... T20)",
    )
    parser.add_argument(
        "--cv", type=str, default=None, help="Path to CV PDF file"
    )
    parser.add_argument(
        "--job", type=str, default=None, help="Path to Job file"
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="Path to candidate profile file",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to archive test results",
    )
    parser.add_argument(
        "--judge-only",
        action="store_true",
        help="Run only the Judge on existing temp/ files",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_JUDGE") or os.getenv("JUDGE_MODEL") or "gemini-3.5-flash-lite",
        help="LLM model",
    )
    args = parser.parse_args()

    if args.judge_only:
        Judge(model=args.model).evaluate(directory=TEMP_DIR)
        return

    # Determine test case configuration
    test_id = args.test_id.upper() if args.test_id else None
    if test_id and test_id in TEST_CASES:
        cv_name, job_name = TEST_CASES[test_id]
        cv_path = PROJECT_ROOT / "tests" / "cvs" / f"cv_{cv_name}.pdf"
        job_path = PROJECT_ROOT / "tests" / "jobs" / f"job_{job_name}.md"
        profile_path = PROJECT_ROOT / "tests" / "profiles" / f"profile_{cv_name}.md"
        output_dir = Path(args.output_dir) if args.output_dir else (RESULTS_DIR / test_id)
    elif args.cv and args.job:
        cv_path = Path(args.cv)
        job_path = Path(args.job)
        profile_path = Path(args.profile) if args.profile else None
        output_dir = Path(args.output_dir) if args.output_dir else None
    else:
        # Default to T01
        test_id = "T01"
        cv_name, job_name = TEST_CASES[test_id]
        cv_path = PROJECT_ROOT / "tests" / "cvs" / f"cv_{cv_name}.pdf"
        job_path = PROJECT_ROOT / "tests" / "jobs" / f"job_{job_name}.md"
        profile_path = PROJECT_ROOT / "tests" / "profiles" / f"profile_{cv_name}.md"
        output_dir = Path(args.output_dir) if args.output_dir else (RESULTS_DIR / test_id)

    run_pipeline(
        cv_path=cv_path,
        job_path=job_path,
        profile_path=profile_path,
        model=args.model,
        output_dir=output_dir,
    )


if __name__ == "__main__":
    main()
