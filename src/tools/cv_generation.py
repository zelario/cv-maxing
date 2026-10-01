"""Deterministic CV rendering from validated structured data."""

from pathlib import Path
import re

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from models.generated_cv import GeneratedCV
from models.cv import StructuredCV
from models.optimization import CVOptimizationResult

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "config" / "cv_template.md.j2"
URL_FIELDS = ("linkedin", "github", "portfolio")


def _candidate_evidence(cv: StructuredCV, optimization: CVOptimizationResult) -> str:
    pieces = [cv.cv]
    pieces.extend(optimization.user_provided_evidence)
    pieces.extend(answer.answer for answer in optimization.user_answers)
    for change in optimization.proposed_changes:
        pieces.extend(change.user_provided_evidence)
    return "\n".join(pieces)


def validate_generated_cv(
    generated: GeneratedCV, cv: StructuredCV, optimization: CVOptimizationResult
) -> GeneratedCV:
    """Validate data and drop URLs that lack verbatim candidate evidence."""
    validated = GeneratedCV.model_validate(generated.model_dump())
    evidence = _candidate_evidence(cv, optimization)
    explicit_consent = re.search(
        r"\bI\s+(?:hereby\s+)?consent\s+to\b|"
        r"\bI\s+agree\s+to\s+the\s+processing\b|"
        r"\bconsinto\s+no\s+tratamento\b",
        evidence,
        flags=re.IGNORECASE,
    )
    if validated.consent and not explicit_consent:
        validated.consent = False
        print("[CV VALIDATION] Removed unsupported GDPR consent")
    for field in URL_FIELDS:
        value = getattr(validated.contact, field)
        if value and value not in evidence:
            setattr(validated.contact, field, None)
            print(f"[CV VALIDATION] Removed unsupported {field} URL")
    for project in validated.projects:
        if project.link and project.link not in evidence:
            project.link = None
            print("[CV VALIDATION] Removed unsupported project URL")
    return validated


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
    generated: GeneratedCV, cv: StructuredCV, optimization: CVOptimizationResult
) -> str:
    return render_cv(validate_generated_cv(generated, cv, optimization))
