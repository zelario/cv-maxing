from enum import Enum

from pydantic import BaseModel, Field


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


class ReviewerResult(BaseModel):
    requirement_matches: list[RequirementMatch] = Field(default_factory=list)

    completeness: list[CompletenessItem] = Field(default_factory=list)

    missing_evidence: list[str] = Field(default_factory=list)

    weak_evidence: list[str] = Field(default_factory=list)

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    overall_assessment: str = ""

    reasoning: str = ""
