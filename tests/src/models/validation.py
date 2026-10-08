from pydantic import BaseModel, Field



class ValidationResult(BaseModel):
    """Structured evaluation of a generated CV."""

    accuracy_score: int = Field(ge=0, le=10)
    job_alignment_score: int = Field(ge=0, le=10)
    completeness_score: int = Field(ge=0, le=10)
    clarity_score: int = Field(ge=0, le=10)
    evidence_score: int = Field(ge=0, le=10)

    hallucinations: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)

