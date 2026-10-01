"""Deterministic CV rendering from structured candidate data."""

from pathlib import Path
import re

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from models.generated_cv import GeneratedCV
from models.job import StructuredJob

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "config" / "cv_template.md.j2"


def _date_sort_key(value: str | None) -> tuple[int, int]:
    """Sort dated entries newest first; undated entries remain at the end."""
    if not value:
        return (0, 0)
    years = [int(year) for year in re.findall(r"\b(?:19|20)\d{2}\b", value)]
    if not years:
        return (0, 0)
    if re.search(r"\b(present|ongoing|current|atualmente|presente)\b", value, re.I):
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
        prepared.contact.specialisation = None
    _sort_chronologically(prepared)
    return prepared


def render_cv(generated: GeneratedCV) -> str:
    """Render the fixed Jinja2 template without adding candidate data."""
    model = GeneratedCV.model_validate(generated.model_dump())
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_PATH.parent)),
        autoescape=False,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    return env.get_template(TEMPLATE_PATH.name).render(**model.model_dump())


def validate_and_render_cv(
    generated: GeneratedCV,
    cv=None,
    optimization=None,
    job: StructuredJob | None = None,
) -> str:
    """Backward-compatible wrapper; applies no evidence-based removals."""
    return render_cv(prepare_generated_cv(generated, job))
