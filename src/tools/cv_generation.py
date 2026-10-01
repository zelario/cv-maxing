"""Deterministic CV rendering from validated structured data."""

from pathlib import Path
import re
from urllib.parse import urlsplit

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from models.generated_cv import GeneratedCV
from models.cv import StructuredCV
from models.optimization import CVOptimizationResult
from models.job import StructuredJob

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "config" / "cv_template.md.j2"
URL_FIELDS = ("linkedin", "github", "portfolio")


def _host_matches(url: str, domain: str) -> bool:
    try:
        parsed = urlsplit(url if "://" in url else f"//{url}")
        host = (parsed.hostname or "").lower().rstrip(".")
    except ValueError:
        return False
    return host == domain or host.endswith(f".{domain}")


def _url_matches_field(field: str, url: str) -> bool:
    if field == "linkedin":
        return _host_matches(url, "linkedin.com")
    if field == "github":
        return _host_matches(url, "github.com")
    if field == "portfolio":
        return not (
            _host_matches(url, "linkedin.com")
            or _host_matches(url, "github.com")
        )
    return False


def _project_link_is_evidenced(
    project_name: str, url: str, cv: StructuredCV, optimization: CVOptimizationResult
) -> bool:
    """Require the exact URL and project name in the same evidence passage."""
    blocks = [cv.cv, *optimization.user_provided_evidence]
    blocks.extend(answer.answer for answer in optimization.user_answers)
    for change in optimization.proposed_changes:
        blocks.extend(change.user_provided_evidence)
    name = project_name.casefold().strip()
    return bool(name) and any(url in block and name in block.casefold() for block in blocks)


def _candidate_evidence(cv: StructuredCV, optimization: CVOptimizationResult) -> str:
    pieces = [cv.cv]
    pieces.extend(optimization.user_provided_evidence)
    pieces.extend(answer.answer for answer in optimization.user_answers)
    for change in optimization.proposed_changes:
        pieces.extend(change.user_provided_evidence)
    return "\n".join(pieces)


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


def _education_grade_is_supported_for_entry(
    item, cv: StructuredCV, optimization: CVOptimizationResult
) -> bool | None:
    """Check grade-to-qualification association when source passages exist."""
    if not item.grade:
        return True
    institution = item.institution.casefold().strip()
    degree = item.degree.casefold().strip()
    if not institution and not degree:
        return None
    source_entries = []
    for entry in cv.education:
        source = " ".join((entry.source_text, entry.details, entry.degree)).casefold()
        if source and ((institution and institution in source) or (degree and degree in source)):
            source_entries.append(source)
    user_entries = [
        f"{answer.question} {answer.answer}".casefold()
        for answer in optimization.user_answers
    ]
    user_entries = [
        answer for answer in user_entries
        if ((institution and institution in answer) or (degree and degree in answer))
    ]
    if not source_entries and not user_entries:
        return None
    grade = item.grade.casefold().strip()
    return any(
        re.search(rf"(?<!\w){re.escape(grade)}(?!\w)", passage)
        for passage in source_entries + user_entries
    )


def _certification_year_is_supported_for_entry(
    item, cv: StructuredCV, optimization: CVOptimizationResult
) -> bool | None:
    if not item.year:
        return True
    name = item.name.casefold().strip()
    issuer = (item.issuer or "").casefold().strip()
    if not name and not issuer:
        return None
    source_entries = []
    for entry in cv.certifications:
        source = " ".join((entry.source_text, entry.name, entry.issuer)).casefold()
        if source and (
            (name and name in source) or (issuer and issuer in source)
        ):
            source_entries.append(source)
    user_entries = [
        f"{answer.question} {answer.answer}".casefold()
        for answer in optimization.user_answers
    ]
    user_entries = [
        answer for answer in user_entries
        if ((name and name in answer) or (issuer and issuer in answer))
    ]
    if not source_entries and not user_entries:
        return None
    year = item.year.casefold().strip()
    return any(
        re.search(rf"(?<!\w){re.escape(year)}(?!\w)", passage)
        for passage in source_entries + user_entries
    )


def validate_generated_cv(
    generated: GeneratedCV,
    cv: StructuredCV,
    optimization: CVOptimizationResult,
    job: StructuredJob | None = None,
) -> GeneratedCV:
    """Validate data and drop URLs that lack verbatim candidate evidence."""
    validated = GeneratedCV.model_validate(generated.model_dump())
    if job and job.job_title.strip():
        validated.contact.headline = job.job_title.strip()
        validated.contact.specialisation = None
    _sort_chronologically(validated)
    for education in validated.education:
        grade_supported = _education_grade_is_supported_for_entry(
            education, cv, optimization
        )
        if grade_supported is False:
            education.grade = None
            print("[CV VALIDATION] Removed grade not evidenced for this qualification")
    for certification in validated.certifications:
        year_supported = _certification_year_is_supported_for_entry(
            certification, cv, optimization
        )
        if year_supported is False:
            certification.year = None
            print("[CV VALIDATION] Removed certification year not evidenced for that credential")
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
    for field in ("location_city", "location_country"):
        value = getattr(validated.contact, field)
        if value and (
            value not in evidence
            or "," in value
            or "\n" in value
            or re.search(r"\d", value)
        ):
            setattr(validated.contact, field, None)
            print(f"[CV VALIDATION] Removed unsupported or overly detailed {field}")
    for field in URL_FIELDS:
        value = getattr(validated.contact, field)
        if value and (value not in evidence or not _url_matches_field(field, value)):
            setattr(validated.contact, field, None)
            print(f"[CV VALIDATION] Removed unsupported or mismatched {field} URL")
    for project in validated.projects:
        if project.link and (
            project.link not in evidence
            or not _project_link_is_evidenced(
                project.name, project.link, cv, optimization
            )
        ):
            project.link = None
            print("[CV VALIDATION] Removed project URL without project-specific evidence")
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
    generated: GeneratedCV,
    cv: StructuredCV,
    optimization: CVOptimizationResult,
    job: StructuredJob | None = None,
) -> str:
    return render_cv(validate_generated_cv(generated, cv, optimization, job))
