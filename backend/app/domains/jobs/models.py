"""Jobs domain models."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Job(BaseModel):
    """Job listing model."""

    id: UUID
    title: str
    company: str
    location: str
    description: str
    requirements: list[str] = Field(default_factory=list)
    salary_range: str | None = None
    job_type: str
    source_url: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
