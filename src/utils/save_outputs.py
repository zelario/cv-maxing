import html
import os
import re
import tempfile
from pathlib import Path

from pydantic import BaseModel

from models.cv import StructuredCV
from models.job import StructuredJob
from models.optimization import CVOptimizationResult
from models.review import ReviewerResult
from models.generated_cv import GeneratedCV, Project

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIRECTORY = PROJECT_ROOT / "temp"
JSON_FILENAMES = {
    "temp_cv.json",
    "temp_job.json",
    "temp_review.json",
    "temp_optimization.json",
    "temp_generated_cv.json",
    "temp_judge.json",
}


def _date_sort_key(value: str | None) -> tuple[int, int]:
    """Sort dated entries newest first; undated entries remain at the end."""
    if not value:
        return (0, 0)
    is_ongoing = bool(
        re.search(r"\b(present|ongoing|current|atualmente|presente)\b", value, re.I)
    )
    years = [int(year) for year in re.findall(r"\b(?:19|20)\d{2}\b", value)]
    if not years:
        return (9999, 9999) if is_ongoing else (0, 0)
    if is_ongoing:
        return (9999, max(years))
    return (max(years), min(years))


def _sort_chronologically(generated: GeneratedCV) -> None:
    generated.experience.sort(key=lambda item: _date_sort_key(item.dates), reverse=True)
    generated.education.sort(key=lambda item: _date_sort_key(item.dates), reverse=True)
    generated.certifications.sort(
        key=lambda item: _date_sort_key(item.year), reverse=True
    )
    generated.projects.sort(key=lambda item: _date_sort_key(item.dates), reverse=True)


def _clean_null_strings(obj):
    """Recursively convert string representations of null/none to None."""
    if isinstance(obj, str):
        if obj.strip().lower() in ("none", "null", "n/a", "na", "undefined"):
            return None
        return obj
    if isinstance(obj, list):
        return [_clean_null_strings(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _clean_null_strings(v) for k, v in obj.items()}
    return obj


def _unescape_strings(obj):
    """Recursively decode HTML entities (&ccedil;, &eacute;, etc.) to clean Unicode."""
    if isinstance(obj, str):
        return html.unescape(obj)
    if isinstance(obj, list):
        return [_unescape_strings(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _unescape_strings(v) for k, v in obj.items()}
    return obj


def prepare_generated_cv(
    generated: GeneratedCV, job: StructuredJob | None = None
) -> GeneratedCV:
    """Copy generated data, then apply deterministic headline, URLs, and ordering."""

    raw_dict = _clean_null_strings(_unescape_strings(generated.model_dump()))
    prepared = GeneratedCV.model_validate(raw_dict)
    # Only fallback to job title if candidate/generator headline is not already set
    if not (prepared.contact.headline and prepared.contact.headline.strip()) and job and job.job_title.strip():
        prepared.contact.headline = job.job_title.strip()
    # Normalize GitHub URL if provided as username or relative path
    if prepared.contact.github:
        gh = prepared.contact.github.strip()
        if not gh.startswith("http://") and not gh.startswith("https://"):
            gh_user = gh.lstrip("/").replace("github.com/", "")
            prepared.contact.github = f"https://github.com/{gh_user}"

    # Ensure project/competition links never leak into contact.portfolio in the header,
    # and deduplicate portfolio if it matches linkedin or github
    if prepared.contact.portfolio:
        portfolio_clean = prepared.contact.portfolio.strip().rstrip("/").lower()
        norm_li = prepared.contact.linkedin.strip().rstrip("/").lower() if prepared.contact.linkedin else ""
        norm_gh = prepared.contact.github.strip().rstrip("/").lower() if prepared.contact.github else ""
        if (norm_li and portfolio_clean == norm_li) or (norm_gh and portfolio_clean == norm_gh):
            prepared.contact.portfolio = None
        else:
            is_project_link = any(
                (p.link and (p.link.strip().rstrip("/").lower() == portfolio_clean or portfolio_clean in p.link.lower() or p.link.lower() in portfolio_clean))
                or (p.description and portfolio_clean in p.description.lower())
                for p in prepared.projects
            )
            if is_project_link:
                prepared.contact.portfolio = None

    # Clean any raw URLs embedded in institution or company names
    for edu in prepared.education:
        if edu.institution:
            edu.institution = re.sub(r"https?://\S+", "", edu.institution).strip()
    for exp in prepared.experience:
        if exp.company:
            exp.company = re.sub(r"https?://\S+", "", exp.company).strip()

    # Volunteering safeguard: relocate any volunteering entries mistakenly placed in experience to projects
    filtered_experience = []
    for exp in prepared.experience:
        text_to_check = f"{exp.title} {exp.company}".lower()
        if any(term in text_to_check for term in ["volunteer", "voluntári", "voluntari"]):
            desc = " ".join(exp.bullets) if exp.bullets else ""
            prepared.projects.append(
                Project(
                    name=exp.title,
                    dates=exp.dates,
                    description=desc,
                    volunteering_or_other="Volunteering",
                )
            )
        else:
            filtered_experience.append(exp)
    prepared.experience = filtered_experience

    _sort_chronologically(prepared)
    return prepared


def save_model_json(model: BaseModel, filename: str, job_id: str | None = None) -> Path:
    """Serialize one validated Pydantic model to an allowed JSON file, optionally isolated by job_id."""

    requested_path = Path(filename)
    if requested_path.name != filename or filename not in JSON_FILENAMES:
        raise ValueError("filename must be one of the supported JSON filenames")

    output_path = DATA_DIRECTORY / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: str | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_path.parent,
            prefix=f".{output_path.stem}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = file.name
            file.write(model.model_dump_json(indent=2))
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, output_path)

        # If job_id is provided, also save an isolated copy for session tracking
        if job_id:
            job_dir = DATA_DIRECTORY / job_id
            job_dir.mkdir(parents=True, exist_ok=True)
            isolated_path = job_dir / filename
            isolated_path.write_text(output_path.read_text(encoding="utf-8"), encoding="utf-8")
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)

    return output_path


def save_pipeline_outputs(result, job_id: str | None = None) -> GeneratedCV:
    """Save validated structured pipeline outputs, optionally isolated by job_id."""

    model_specs = [
        ("temp_cv.json", StructuredCV),
        ("temp_job.json", StructuredJob),
        ("temp_review.json", ReviewerResult),
        ("temp_optimization.json", CVOptimizationResult),
    ]

    task_outputs = getattr(result, "tasks_output", [])
    outputs_by_model: dict[type[BaseModel], BaseModel] = {}

    for t in task_outputs:
        pydantic_obj = getattr(t, "pydantic", None)
        if pydantic_obj is not None:
            for _, model_cls in model_specs:
                if isinstance(pydantic_obj, model_cls):
                    outputs_by_model[model_cls] = pydantic_obj
            if isinstance(pydantic_obj, GeneratedCV):
                outputs_by_model[GeneratedCV] = pydantic_obj

    # Positional fallback if any model was not identified by type
    fallback_models = [
        StructuredCV,
        StructuredJob,
        ReviewerResult,
        CVOptimizationResult,
        GeneratedCV,
    ]
    for idx, model_cls in enumerate(fallback_models):
        if model_cls not in outputs_by_model and idx < len(task_outputs):
            obj = getattr(task_outputs[idx], "pydantic", None)
            if isinstance(obj, model_cls):
                outputs_by_model[model_cls] = obj

    for filename, model_cls in model_specs:
        output = outputs_by_model.get(model_cls)
        if output is None:
            raise TypeError(f"Pipeline did not return {model_cls.__name__}")
        save_model_json(output, filename, job_id=job_id)

    raw_generated = outputs_by_model.get(GeneratedCV)
    if not isinstance(raw_generated, GeneratedCV):
        raise TypeError("Pipeline did not return GeneratedCV")

    job_output = outputs_by_model.get(StructuredJob)
    generated = prepare_generated_cv(
        raw_generated, job_output if isinstance(job_output, StructuredJob) else None
    )
    save_model_json(generated, "temp_generated_cv.json", job_id=job_id)

    print("[PIPELINE] Structured CV, job, review, optimization, and generated CV saved")
    return generated
