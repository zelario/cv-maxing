from pydantic import BaseModel, Field, field_validator
from pathlib import Path
import json
from crewai.tools import tool


class RequirementMatch(BaseModel):
    requirement: str = ""
    category: str = ""
    status: str = ""
    match_score: float = 0.0
    evidence: list[str] = Field(default_factory=list)
    reasoning: str = ""

    @field_validator("match_score", mode="before")
    @classmethod
    def handle_null_score(cls, value):
        if value is None:
            return 0.0
        return value


class CriterionScore(BaseModel):
    criterion: str = ""
    score: float = 0.0
    evidence: list[str] = Field(default_factory=list)

    @field_validator("score", mode="before")
    @classmethod
    def handle_null_score(cls, value):
        if value is None:
            return 0.0
        return value


class Improvement(BaseModel):
    priority: str = ""
    problem: str = ""
    evidence: list[str] = Field(default_factory=list)
    recommendation: str = ""
    expected_impact: str = ""


class ReviewerResult(BaseModel):
    deterministic_score: float = 0.0
    ai_assessment: float = 0.0

    criterion_scores: list[CriterionScore] = Field(
        default_factory=list
    )

    requirement_matches: list[RequirementMatch] = Field(
        default_factory=list
    )

    missing_requirements: list[str] = Field(
        default_factory=list
    )

    weak_evidence: list[str] = Field(
        default_factory=list
    )

    strengths: list[str] = Field(
        default_factory=list
    )

    improvements: list[Improvement] = Field(
        default_factory=list
    )

    reasoning: str = ""

    score_disagreement: str = ""