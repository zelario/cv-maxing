from models.cv import StructuredCV
from models.generated_cv import ContactInfo, GeneratedCV, Skills
from models.optimization import CVOptimizationResult, ProposedCVChange
from tools.cv_generation import validate_and_render_cv


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
    languages = result.split("## LANGUAGES", 1)[1].split("---", 1)[0]
    certifications = result.split(
        "## CERTIFICATIONS AND ADDITIONAL TRAINING", 1
    )[1].split("---", 1)[0]
    assert not languages.strip()
    assert not certifications.strip()
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
    result = validate_and_render_cv(
        generated(), StructuredCV(cv="Ada Lovelace"), CVOptimizationResult()
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
