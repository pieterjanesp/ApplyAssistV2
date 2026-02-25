"""Jobs domain request/response schemas."""

from pydantic import BaseModel

from app.domains.jobs.models import Job


class JobCreate(BaseModel):
    """Schema for creating a new job listing."""

    title: str
    company: str
    location: str
    description: str
    requirements: list[str] = []
    salary_range: str | None = None
    job_type: str
    source_url: str | None = None


class JobSearchParams(BaseModel):
    """Query parameters for searching/filtering jobs."""

    query: str | None = None
    location: str | None = None
    job_type: str | None = None


class JobResponse(Job):
    """Job response schema."""

    pass


class JobMatchScore(BaseModel):
    """Score representing how well a job matches a user's profile."""

    job_id: str
    score: float
