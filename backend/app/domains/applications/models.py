"""Applications domain models."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class ApplicationStatus(str, Enum):
    """Allowed application statuses."""

    DRAFT = "draft"
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(BaseModel):
    """Job application model."""

    id: UUID
    user_id: str
    job_id: str
    cv_id: str | None = None
    cover_letter_id: str | None = None
    status: ApplicationStatus = ApplicationStatus.DRAFT
    applied_at: datetime | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
