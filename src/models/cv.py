from pydantic import BaseModel, Field


class CVPersonalInformation(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    nationality: str = ""
    date_of_birth: str = ""
    source_section: str = ""
    source_text: str = ""


class CVSkill(BaseModel):
    name: str = ""
    source_section: str = ""
    source_text: str = ""


class CVEducation(BaseModel):
    level: str = ""
    degree: str = ""
    field: str = ""
    institution: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    details: str = ""
    source_section: str = ""
    source_text: str = ""


class CVExperience(BaseModel):
    job_title: str = ""
    company: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    description: str = ""
    responsibilities: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    skills_evidenced: list[str] = Field(default_factory=list)
    source_section: str = ""
    source_text: str = ""


class CVProject(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    skills_evidenced: list[str] = Field(default_factory=list)
    source_section: str = ""
    source_text: str = ""


class CVCertification(BaseModel):
    name: str = ""
    issuer: str = ""
    date: str = ""
    source_section: str = ""
    source_text: str = ""


class CVLanguage(BaseModel):
    language: str = ""
    proficiency: str = ""
    source_section: str = ""
    source_text: str = ""


class CVAchievement(BaseModel):
    description: str = ""
    date: str = ""
    source_section: str = ""
    source_text: str = ""


class CVOther(BaseModel):
    type: str = ""
    content: str = ""
    source_section: str = ""
    source_text: str = ""


class CVSummary(BaseModel):
    text: str = ""
    source_section: str = ""
    source_text: str = ""


class StructuredCV(BaseModel):
    cv: str = ""

    personal_information: CVPersonalInformation = Field(
        default_factory=CVPersonalInformation
    )

    summary: CVSummary = Field(default_factory=CVSummary)

    education: list[CVEducation] = Field(default_factory=list)

    experience: list[CVExperience] = Field(default_factory=list)

    skills: list[CVSkill] = Field(default_factory=list)

    projects: list[CVProject] = Field(default_factory=list)

    certifications: list[CVCertification] = Field(default_factory=list)

    languages: list[CVLanguage] = Field(default_factory=list)

    achievements: list[CVAchievement] = Field(default_factory=list)

    other: list[CVOther] = Field(default_factory=list)
