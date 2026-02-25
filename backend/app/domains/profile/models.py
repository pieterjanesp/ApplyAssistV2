"""Profile domain models."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """Core user profile model."""

    id: UUID
    user_id: str
    full_name: str
    email: str
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience_years: int | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WorkExperience(BaseModel):
    """Work experience record."""

    id: UUID
    user_id: str
    job_title: str
    company: str
    start_date: str | None = None
    end_date: str | None = None
    is_current: bool = False
    description: str | None = None
    achievements: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Education(BaseModel):
    """Education record."""

    id: UUID
    user_id: str
    institution: str
    degree: str
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CareerGoals(BaseModel):
    """Career goals record."""

    id: UUID
    user_id: str
    target_roles: list[str] = Field(default_factory=list)
    target_industries: list[str] = Field(default_factory=list)
    career_narrative: str | None = None
    motivations: str | None = None
    preferred_work_style: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
