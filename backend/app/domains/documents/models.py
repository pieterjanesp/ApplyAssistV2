"""Documents domain models for CVs and cover letters."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class SectionType(str, Enum):
    """Allowed CV section types."""

    EXPERIENCE = "experience"
    EDUCATION = "education"
    SKILLS = "skills"
    PROJECTS = "projects"
    CERTIFICATIONS = "certifications"
    CUSTOM = "custom"


class CVItem(BaseModel):
    """A single item within a CV section."""

    id: UUID
    content: str
    order: int


class CVSection(BaseModel):
    """A section of a CV containing ordered items."""

    id: UUID
    title: str
    section_type: SectionType
    items: list[CVItem] = Field(default_factory=list)
    order: int


class CV(BaseModel):
    """Full CV model with nested sections."""

    id: UUID
    user_id: str
    title: str
    sections: list[CVSection] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CoverLetter(BaseModel):
    """Cover letter model."""

    id: UUID
    user_id: str
    job_id: str | None = None
    content: str
    tone: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
