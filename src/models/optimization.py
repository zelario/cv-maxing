from typing import Literal

from pydantic import BaseModel, Field

EvidenceSource = Literal["cv", "user", "cv_and_user"]


class ProposedCVChange(BaseModel):
    section: str = ""
    current_content: str = ""
    proposed_content: str = ""
    rationale: str = ""
    evidence_source: EvidenceSource = "cv"
    source_evidence: list[str] = Field(default_factory=list)
    user_provided_evidence: list[str] = Field(default_factory=list)
    requires_human_approval: bool = True


class UserAnswer(BaseModel):
    question: str = ""
    answer: str = ""
    gap: str = ""
    resolution: Literal["supported", "unsupported", "not_applicable", "unresolved"] = "unresolved"


class CVOptimizationResult(BaseModel):
    proposed_changes: list[ProposedCVChange] = Field(default_factory=list)
    questions_asked: list[str] = Field(default_factory=list)
    user_answers: list[UserAnswer] = Field(default_factory=list)
    user_provided_evidence: list[str] = Field(default_factory=list)
    optimization_strategy: str = ""
    unresolved_evidence_gaps: list[str] = Field(default_factory=list)
