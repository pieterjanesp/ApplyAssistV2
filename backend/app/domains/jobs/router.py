"""Jobs domain API routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_current_user
from app.domains.jobs.schemas import (
    JobCreate,
    JobMatchScore,
    JobResponse,
    JobSearchParams,
)
from app.domains.jobs.service import JobService

router = APIRouter(tags=["jobs"])


def _get_service() -> JobService:
    return JobService()


@router.get("/", response_model=list[JobResponse])
async def list_jobs(
    query: str | None = Query(default=None, description="Search query"),
    location: str | None = Query(default=None, description="Location filter"),
    job_type: str | None = Query(default=None, description="Job type filter"),
    user_id: str = Depends(get_current_user),
    service: JobService = Depends(_get_service),
) -> list[JobResponse]:
    """List or search job listings."""
    params = JobSearchParams(query=query, location=location, job_type=job_type)
    jobs = service.get_jobs(params)
    return [JobResponse(**j.model_dump()) for j in jobs]


@router.get("/match/profile", response_model=list[JobMatchScore])
async def match_jobs_to_profile(
    user_id: str = Depends(get_current_user),
    service: JobService = Depends(_get_service),
) -> list[JobMatchScore]:
    """Get jobs matched to the current user's profile (placeholder)."""
    return service.match_jobs_to_profile(user_id)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    user_id: str = Depends(get_current_user),
    service: JobService = Depends(_get_service),
) -> JobResponse:
    """Get a specific job listing by ID."""
    job = service.get_job(job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )
    return JobResponse(**job.model_dump())


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    data: JobCreate,
    user_id: str = Depends(get_current_user),
    service: JobService = Depends(_get_service),
) -> JobResponse:
    """Create a new job listing."""
    job = service.create_job(data)
    return JobResponse(**job.model_dump())
