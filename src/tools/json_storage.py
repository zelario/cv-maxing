import json
import os
import tempfile
from pathlib import Path
from typing import Any

from crewai.tools import tool

DATA_DIRECTORY = Path("temp")

def save_json_object(payload: Any, path: Path) -> dict[str, Any]:
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
    if requested_path.name != filename or requested_path.suffix.lower() != ".json":
        raise ValueError("filename must be a JSON filename inside the data directory")

    output_path = DATA_DIRECTORY / requested_path.name
    save_json_object(payload, output_path)
    message = f"[TOOL] JSON saved to {output_path}"
    print(message)
    return message
