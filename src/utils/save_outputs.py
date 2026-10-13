import os
import re
import tempfile
from pathlib import Path

from pydantic import BaseModel

from models.cv import StructuredCV
from models.job import StructuredJob
from models.optimization import CVOptimizationResult
from models.review import ReviewerResult
from models.generated_cv import GeneratedCV

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


def prepare_generated_cv(
    generated: GeneratedCV, job: StructuredJob | None = None
) -> GeneratedCV:
    """Copy generated data, then apply deterministic headline and ordering."""

    prepared = GeneratedCV.model_validate(generated.model_dump())
    if job and job.job_title.strip():
        prepared.contact.headline = job.job_title.strip()
    _sort_chronologically(prepared)
    return prepared


def save_model_json(model: BaseModel, filename: str) -> Path:
    """Serialize one validated Pydantic model to an allowed JSON file."""

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
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)

    return output_path


def save_pipeline_outputs(result) -> GeneratedCV:
    """Save validated structured pipeline outputs."""

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
        save_model_json(output, filename)

    raw_generated = outputs_by_model.get(GeneratedCV)
    if not isinstance(raw_generated, GeneratedCV):
        raise TypeError("Pipeline did not return GeneratedCV")

    job_output = outputs_by_model.get(StructuredJob)
    generated = prepare_generated_cv(
        raw_generated, job_output if isinstance(job_output, StructuredJob) else None
    )
    save_model_json(generated, "temp_generated_cv.json")

    print("[PIPELINE] Structured CV, job, review, optimization, and generated CV saved")
    return generated
