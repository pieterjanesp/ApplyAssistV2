"""Profile domain request/response schemas."""

from pydantic import BaseModel

from app.domains.profile.models import UserProfile


class ProfileCreate(BaseModel):
    """Schema for creating a new profile."""

    full_name: str
    email: str
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    skills: list[str] = []
    experience_years: int | None = None


class ProfileUpdate(BaseModel):
    """Schema for updating an existing profile. All fields are optional."""

    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    skills: list[str] | None = None
    experience_years: int | None = None


class ProfileResponse(UserProfile):
    """Profile response schema."""

    pass
