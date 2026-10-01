import os
import tempfile
from pathlib import Path

from pydantic import BaseModel

from models.cv import StructuredCV
from models.job import StructuredJob
from models.optimization import CVOptimizationResult
from models.review import ReviewerResult
from models.generated_cv import GeneratedCV
from tools.cv_generation import validate_generated_cv


DATA_DIRECTORY = Path("temp")
JSON_FILENAMES = {
    "structured_cv_temp.json",
    "structured_job_temp.json",
    "structured_review_temp.json",
    "structured_optimization_temp.json",
    "generated_cv_temp.json",
}


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


def save_markdown(content: str, filename: str = "optimized_cv.md") -> Path:
    """Write deterministic rendered CV Markdown atomically to temp."""

    if filename != "optimized_cv.md":
        raise ValueError("filename must be optimized_cv.md")

    output_path = DATA_DIRECTORY / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: str | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_path.parent,
            prefix=".optimized_cv.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = file.name
            file.write(content)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, output_path)
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)

    return output_path


def save_pipeline_outputs(result) -> None:
    """Save validated structured pipeline outputs."""

    outputs = [
        (0, "structured_cv_temp.json", StructuredCV),
        (1, "structured_job_temp.json", StructuredJob),
        (2, "structured_review_temp.json", ReviewerResult),
        (3, "structured_optimization_temp.json", CVOptimizationResult),
    ]

    for task_index, filename, model in outputs:
        output = result.tasks_output[task_index].pydantic
        if not isinstance(output, model):
            raise TypeError(f"Task {task_index} did not return {model.__name__}")
        save_model_json(output, filename)

    generated = result.tasks_output[4].pydantic
    if not isinstance(generated, GeneratedCV):
        raise TypeError("Task 4 did not return GeneratedCV")
    generated = validate_generated_cv(
        generated,
        result.tasks_output[0].pydantic,
        result.tasks_output[3].pydantic,
    )
    save_model_json(generated, "generated_cv_temp.json")

    print("[PIPELINE] Structured CV, job, review, optimization, and generated CV saved")
