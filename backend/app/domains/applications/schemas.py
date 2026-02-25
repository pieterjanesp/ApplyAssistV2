"""Applications domain request/response schemas."""

from pydantic import BaseModel

from app.domains.applications.models import Application, ApplicationStatus


class ApplicationCreate(BaseModel):
    """Schema for creating a new application."""

    job_id: str
    cv_id: str | None = None
    cover_letter_id: str | None = None
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    """Schema for updating an application."""

    status: ApplicationStatus | None = None
    notes: str | None = None


class ApplicationResponse(Application):
    """Application response schema."""

    pass
