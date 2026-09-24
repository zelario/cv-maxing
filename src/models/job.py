from enum import Enum
from pydantic import BaseModel, Field


class RequirementType(str, Enum):
    REQUIRED = "required"
    PREFERRED = "preferred"


class JobSkill(BaseModel):
    name: str = ""
    requirement_type: RequirementType = RequirementType.REQUIRED
    source_section: str = ""
    source_text: str = ""


class JobExperienceRequirement(BaseModel):
    description: str = ""
    years: str = ""
    requirement_type: RequirementType = RequirementType.REQUIRED
    source_section: str = ""
    source_text: str = ""


class JobEducationRequirement(BaseModel):
    level: str = ""
    degree: str = ""
    field: str = ""
    requirement_type: RequirementType = RequirementType.REQUIRED
    source_section: str = ""
    source_text: str = ""


class JobResponsibility(BaseModel):
    description: str = ""
    source_section: str = ""
    source_text: str = ""


class JobKeyword(BaseModel):
    keyword: str = ""
    source_section: str = ""
    source_text: str = ""


class JobOtherRequirement(BaseModel):
    type: str = ""
    description: str = ""
    requirement_type: RequirementType = RequirementType.REQUIRED
    source_section: str = ""
    source_text: str = ""


class JobCompany(BaseModel):
    name: str = ""
    location: str = ""
    website: str = ""


class StructuredJob(BaseModel):
    job_title: str = ""

    company: JobCompany = Field(default_factory=JobCompany)

    location: str = ""

    employment_type: str = ""

    seniority: str = ""

    description: str = ""

    skills: list[JobSkill] = Field(default_factory=list)

    experience_requirements: list[JobExperienceRequirement] = Field(
        default_factory=list
    )

    education_requirements: list[JobEducationRequirement] = Field(default_factory=list)

    responsibilities: list[JobResponsibility] = Field(default_factory=list)

    keywords: list[JobKeyword] = Field(default_factory=list)

    other_requirements: list[JobOtherRequirement] = Field(default_factory=list)
