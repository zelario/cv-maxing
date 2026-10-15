from pydantic import BaseModel, ConfigDict, Field


class ContactInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    headline: str | None = None
    specialisation: str | None = None
    phone: str | None = None
    email: str | None = None
    location_city: str | None = None
    location_country: str | None = None
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None


class ExperienceItem(BaseModel):
    title: str
    dates: str
    company: str
    location: str | None = None
    bullets: list[str] = Field(default_factory=list)


class EducationItem(BaseModel):
    degree: str
    dates: str
    institution: str
    location: str | None = None
    grade: str | None = None


class SkillCategory(BaseModel):
    category_name: str
    skills: list[str] = Field(default_factory=list)


class Language(BaseModel):
    name: str
    level: str | None = None
    details: str | None = None
    certification: str | None = None


class Certification(BaseModel):
    name: str
    issuer: str | None = None
    year: str | None = None


class Project(BaseModel):
    name: str
    dates: str | None = None
    description: str | None = None
    link: str | None = None
    volunteering_or_other: str | None = None


class GeneratedCV(BaseModel):
    contact: ContactInfo
    summary: str | None = None
    experience: list[ExperienceItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    skills: list[SkillCategory] = Field(default_factory=list)
    languages: list[Language] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    consent: bool = False
