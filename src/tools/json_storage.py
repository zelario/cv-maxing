import json
import os
import tempfile
from pathlib import Path
from typing import Any

from crewai.tools import tool
from pydantic import BaseModel

from models.cv import StructuredCV
from models.job import StructuredJob
from models.optimization import CVOptimizationResult
from models.review import ReviewerResult

DATA_DIRECTORY = Path("temp")

JSON_MODELS: dict[str, type[BaseModel]] = {
    "structured_cv_temp.json": StructuredCV,
    "structured_job_temp.json": StructuredJob,
    "structured_review_temp.json": ReviewerResult,
    "structured_optimization_temp.json": CVOptimizationResult,
}

JSON_MARKER_KEYS: dict[str, set[str]] = {
    "structured_cv_temp.json": {"cv", "personal_information", "education"},
    "structured_job_temp.json": {"job_title", "company", "skills"},
    "structured_review_temp.json": {"requirement_matches", "missing_evidence"},
    "structured_optimization_temp.json": {
        "optimized_cv_markdown",
        "proposed_changes",
    },
}

def save_json_object(
    payload: Any,
    path: Path,
    model: type[BaseModel] | None = None,
) -> dict[str, Any]:
    """Normalize a JSON object and write it atomically to disk."""

    if isinstance(payload, str):
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as error:
            raise ValueError("The payload is not valid JSON.") from error
    elif isinstance(payload, dict):
        data = payload
    else:
        raise TypeError("The payload must be a JSON object or a JSON string.")

    if not isinstance(data, dict):
        raise TypeError("The JSON payload must contain an object at the top level.")

    expected_keys = JSON_MARKER_KEYS[path.name]
    if not expected_keys.intersection(data):
        raise ValueError(
            f"Payload does not match the expected schema for {path.name}."
        )

    if model is not None:
        data = model.model_validate(data).model_dump(mode="json")

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: str | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.stem}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = file.name
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, path)
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)

    return data


@tool("save_json")
def save_json(payload: Any, filename: str) -> str:
    """
    Save a JSON object or JSON string in the data directory.
    """

    requested_path = Path(filename)
    if requested_path.name != filename or requested_path.name not in JSON_MODELS:
        raise ValueError(
            "filename must be one of the supported structured JSON filenames"
        )

    output_path = DATA_DIRECTORY / requested_path.name
    save_json_object(payload, output_path, JSON_MODELS[requested_path.name])
    message = f"[TOOL] JSON saved to {output_path}"
    print(message)
    return message


@tool("load_json")
def load_json(filename: str) -> str:
    """Load a previously saved structured JSON result when it exists."""

    requested_path = Path(filename)
    if requested_path.name != filename or requested_path.name not in JSON_MODELS:
        raise ValueError(
            "filename must be one of the supported structured JSON filenames"
        )

    output_path = DATA_DIRECTORY / requested_path.name
    if not output_path.exists():
        return "{}"

    return output_path.read_text(encoding="utf-8")
