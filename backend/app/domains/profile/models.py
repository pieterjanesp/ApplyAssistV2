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
