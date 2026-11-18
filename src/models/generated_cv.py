import re
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def _clean_str(v: Any) -> Any:
    if isinstance(v, str) and v.strip().lower() in ("none", "null", "n/a", "na", "undefined"):
        return None
    return v


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

    @field_validator(
        "headline",
        "specialisation",
        "phone",
        "email",
        "location_city",
        "location_country",
        "linkedin",
        "github",
        "portfolio",
        mode="before",
    )
    @classmethod
    def clean_optional_strings(cls, v: Any) -> Any:
        return _clean_str(v)

    @model_validator(mode="after")
    def deduplicate_links(self) -> "ContactInfo":
        norm_li = self.linkedin.strip().rstrip("/").lower() if self.linkedin else None
        norm_gh = self.github.strip().rstrip("/").lower() if self.github else None
        if self.portfolio:
            norm_p = self.portfolio.strip().rstrip("/").lower()
            if (norm_li and norm_p == norm_li) or (norm_gh and norm_p == norm_gh):
                self.portfolio = None
        if self.github and norm_gh and norm_li and norm_gh == norm_li:
            self.github = None
        return self


class ExperienceItem(BaseModel):
    title: str
    dates: str
    company: str
    location: str | None = None
    bullets: list[str] = Field(default_factory=list)

    @field_validator("location", mode="before")
    @classmethod
    def clean_optional_strings(cls, v: Any) -> Any:
        return _clean_str(v)


class EducationItem(BaseModel):
    degree: str
    dates: str
    institution: str
    location: str | None = None
    grade: str | None = None

    @field_validator("location", "grade", mode="before")
    @classmethod
    def clean_optional_strings(cls, v: Any) -> Any:
        return _clean_str(v)


class SkillCategory(BaseModel):
    category_name: str
    skills: list[str] = Field(default_factory=list)


class Language(BaseModel):
    name: str
    level: str | None = None
    details: str | None = None
    certification: str | None = None

    @field_validator("level", "details", "certification", mode="before")
    @classmethod
    def clean_optional_strings(cls, v: Any) -> Any:
        return _clean_str(v)

    @model_validator(mode="after")
    def deduplicate_fields(self) -> "Language":
        # Clean certification redundancy
        if self.certification:
            c_low = self.certification.strip().lower()
            l_low = (self.level or "").strip().lower()
            if c_low in ("native", "none", "null", "n/a") or c_low == l_low or c_low in l_low.split():
                self.certification = None

        # Clean details redundancy
        if self.details:
            d_low = self.details.strip().lower()
            l_low = (self.level or "").strip().lower()
            if "native" in l_low and any(w in d_low for w in ["native", "materna", "mother tongue"]):
                self.details = None
            elif d_low == l_low:
                self.details = None
            else:
                filler = {"proficiency", "speaker", "level", "language", "proficient", "advanced", "working", "professional", "full"}
                d_words = set(re.findall(r"\b\w+\b", d_low)) - filler
                l_words = set(re.findall(r"\b\w+\b", l_low)) - filler
                specific_context = any(term in d_low for term in ["legal", "medical", "clinical", "contract", "drafting", "negotiation", "technical"])
                if not specific_context and (not d_words or d_words.issubset(l_words)):
                    self.details = None

        return self


class Certification(BaseModel):
    name: str
    issuer: str | None = None
    year: str | None = None

    @field_validator("issuer", "year", mode="before")
    @classmethod
    def clean_optional_strings(cls, v: Any) -> Any:
        return _clean_str(v)


class Project(BaseModel):
    name: str
    dates: str | None = None
    description: str | None = None
    link: str | None = None
    volunteering_or_other: str | None = None

    @field_validator("dates", "description", "link", "volunteering_or_other", mode="before")
    @classmethod
    def clean_optional_strings(cls, v: Any) -> Any:
        return _clean_str(v)


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

    @field_validator("summary", mode="before")
    @classmethod
    def clean_optional_strings(cls, v: Any) -> Any:
        return _clean_str(v)

