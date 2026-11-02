from enum import Enum

from pydantic import BaseModel, Field, field_validator


def _as_text(value):
    """Normalize common list-shaped LLM output for scalar text fields."""
    if isinstance(value, list):
        return "\n".join(str(item) for item in value if item is not None)
    if value is None:
        return ""
    return value


class EvidenceStatus(str, Enum):
    SATISFIED = "satisfied"
    WEAK_EVIDENCE = "weak_evidence"
    NO_EVIDENCE = "no_evidence"
    UNCERTAIN = "uncertain"


class RequirementMatch(BaseModel):
    requirement: str = ""
    category: str = ""
    status: EvidenceStatus = EvidenceStatus.NO_EVIDENCE

    evidence: list[str] = Field(default_factory=list)

    reasoning: str = ""

    @field_validator("reasoning", mode="before")
    @classmethod
    def normalize_reasoning(cls, value):
        return _as_text(value)


class CompletenessStatus(str, Enum):
    PRESENT = "present"
    MISSING = "missing"
    UNCERTAIN = "uncertain"


class CompletenessItem(BaseModel):
    section: str = ""
    field: str = ""
    status: CompletenessStatus = CompletenessStatus.MISSING
    evidence: list[str] = Field(default_factory=list)
    relevance: str = ""
    reasoning: str = ""

    @field_validator("relevance", "reasoning", mode="before")
    @classmethod
    def normalize_text_fields(cls, value):
        return _as_text(value)


class ReviewerResult(BaseModel):
    requirement_matches: list[RequirementMatch] = Field(default_factory=list)

    completeness: list[CompletenessItem] = Field(default_factory=list)

    missing_evidence: list[str] = Field(default_factory=list)

    weak_evidence: list[str] = Field(default_factory=list)

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    overall_assessment: str = ""

    reasoning: str = ""

    @field_validator("overall_assessment", "reasoning", mode="before")
    @classmethod
    def normalize_text_fields(cls, value):
        return _as_text(value)
