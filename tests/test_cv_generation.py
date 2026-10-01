from models.cv import StructuredCV
from models.generated_cv import (
    Certification,
    ContactInfo,
    EducationItem,
    ExperienceItem,
    GeneratedCV,
    Language,
    Project,
    Skills,
)
from models.optimization import CVOptimizationResult, ProposedCVChange
from tools.cv_generation import validate_and_render_cv
import pytest
from pydantic import ValidationError


def generated(**contact_fields):
    return GeneratedCV(
        contact=ContactInfo(name="Ada Lovelace", **contact_fields),
        skills=Skills(),
    )


def test_absent_github_is_not_rendered():
    result = validate_and_render_cv(
        generated(), StructuredCV(cv="Ada Lovelace"), CVOptimizationResult()
    )
    assert "github.com" not in result.lower()


def test_exact_source_url_is_rendered():
    url = "https://github.com/ada"
    result = validate_and_render_cv(
        generated(github=url),
        StructuredCV(cv=f"GitHub: {url}"),
        CVOptimizationResult(),
    )
    assert url in result


def test_exact_github_url_without_scheme_is_still_a_github_url():
    url = "github.com/ada"
    result = validate_and_render_cv(
        generated(github=url),
        StructuredCV(cv=f"GitHub: {url}"),
        CVOptimizationResult(),
    )
    assert url in result


def test_unsupported_profile_urls_are_removed():
    result = validate_and_render_cv(
        generated(
            linkedin="https://linkedin.com/in/ada",
            github="https://github.com/ada",
            portfolio="https://ada.dev",
        ),
        StructuredCV(cv="Ada Lovelace"),
        CVOptimizationResult(),
    )
    for url in ("linkedin.com", "github.com", "ada.dev"):
        assert url not in result


def test_github_url_is_not_reused_as_linkedin_or_portfolio():
    url = "https://github.com/ada"
    result = validate_and_render_cv(
        generated(linkedin=url, github=url, portfolio=url),
        StructuredCV(cv=f"GitHub profile: {url}"),
        CVOptimizationResult(),
    )
    assert result.count(url) == 1


def test_project_url_requires_evidence_associated_with_that_project():
    url = "https://github.com/ada"
    cv = generated()
    cv.projects = [Project(name="Hackathon Alpha", link=url)]
    result = validate_and_render_cv(
        cv, StructuredCV(cv=f"GitHub profile: {url}"), CVOptimizationResult()
    )
    assert url not in result

    result = validate_and_render_cv(
        cv,
        StructuredCV(cv=f"Hackathon Alpha project: {url}"),
        CVOptimizationResult(),
    )
    assert url in result


def test_contact_location_only_contains_city_and_country():
    result = validate_and_render_cv(
        generated(location_city="Coimbra", location_country="Portugal"),
        StructuredCV(cv="Address: Rua A, 123, Coimbra, Portugal"),
        CVOptimizationResult(),
    )
    assert "Coimbra, Portugal" in result
    assert "Rua A" not in result
    assert "123" not in result


def test_unsupported_location_components_are_removed():
    result = validate_and_render_cv(
        generated(location_city="Lisbon", location_country="Portugal"),
        StructuredCV(cv="Address: Coimbra, Portugal"),
        CVOptimizationResult(),
    )
    assert "Lisbon" not in result
    assert "Portugal" in result


def test_free_form_address_field_is_not_allowed():
    with pytest.raises(ValidationError):
        ContactInfo.model_validate(
            {"name": "Ada Lovelace", "location": "10 Downing Street, London"}
        )


def test_consent_is_not_inferred_from_missing_evidence():
    cv = generated()
    cv.consent = True
    result = validate_and_render_cv(cv, StructuredCV(cv="Ada Lovelace"), CVOptimizationResult())
    assert "I consent to the processing" not in result


def test_explicit_consent_is_rendered():
    cv = generated()
    cv.consent = True
    result = validate_and_render_cv(
        cv,
        StructuredCV(cv="I consent to the processing of my personal data."),
        CVOptimizationResult(),
    )
    assert "I consent to the processing" in result


def test_missing_languages_and_certifications_stay_empty():
    result = validate_and_render_cv(
        generated(), StructuredCV(cv="Ada Lovelace"), CVOptimizationResult()
    )
    assert "## LANGUAGES" not in result
    assert "## CERTIFICATIONS AND ADDITIONAL TRAINING" not in result
    assert "native" not in result
    assert "C1" not in result


def test_optimizer_change_can_appear_when_supported():
    change = ProposedCVChange(
        section="Skills",
        proposed_content="Python",
        evidence_source="cv",
        source_evidence=["Python"],
    )
    cv = generated()
    cv.skills.technical.append("Python")
    result = validate_and_render_cv(
        cv,
        StructuredCV(cv="Python"),
        CVOptimizationResult(proposed_changes=[change]),
    )
    assert "**Technical:** Python" in result


def test_template_keeps_fixed_section_order():
    cv = generated(location_city="Coimbra", location_country="Portugal")
    cv.summary = "Evidence-backed summary."
    cv.skills.technical = ["Python"]
    cv.experience = [ExperienceItem(title="Analyst", dates="2024", company="Example")]
    cv.education = [EducationItem(degree="BSc", dates="2020–2024", institution="Example U")]
    cv.languages = [Language(name="English", level="C1")]
    cv.certifications = [Certification(name="Certificate", issuer="Provider", year="2024")]
    cv.projects = [Project(name="Project", description="Evidence-backed description.")]
    result = validate_and_render_cv(
        cv, StructuredCV(cv="Ada Lovelace"), CVOptimizationResult()
    )
    headings = [
        "## PROFESSIONAL SUMMARY",
        "## PROFESSIONAL EXPERIENCE",
        "## EDUCATION",
        "## SKILLS",
        "## LANGUAGES",
        "## CERTIFICATIONS AND ADDITIONAL TRAINING",
        "## PROJECTS, VOLUNTEERING AND OTHER (OPTIONAL)",
    ]
    assert [result.index(item) for item in headings] == sorted(
        result.index(item) for item in headings
    )
    assert "<!--" not in result
    assert "[Relevant certification]" not in result
