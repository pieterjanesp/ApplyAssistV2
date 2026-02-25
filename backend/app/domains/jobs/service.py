"""Jobs domain service with placeholder implementations."""

from datetime import datetime, timezone
from uuid import uuid4

from app.domains.jobs.models import Job
from app.domains.jobs.schemas import JobCreate, JobMatchScore, JobSearchParams


def _mock_job(title: str = "Software Engineer", company: str = "Acme Corp") -> Job:
    """Create a mock job for placeholder responses."""
    return Job(
        id=uuid4(),
        title=title,
        company=company,
        location="Remote",
        description="We are looking for a talented software engineer to join our team.",
        requirements=["Python", "FastAPI", "PostgreSQL", "3+ years experience"],
        salary_range="$100k - $140k",
        job_type="full-time",
        source_url="https://example.com/jobs/1",
        created_at=datetime.now(tz=timezone.utc),
    )


class JobService:
    """Service for job listing management and matching."""

    def get_jobs(self, params: JobSearchParams) -> list[Job]:
        """List/search jobs with optional filters. Placeholder implementation."""
        jobs = [
            _mock_job("Software Engineer", "Acme Corp"),
            _mock_job("Backend Developer", "Widgets Inc"),
        ]

        # Apply basic filtering on mock data
        if params.query:
            query_lower = params.query.lower()
            jobs = [j for j in jobs if query_lower in j.title.lower()]
        if params.location:
            loc_lower = params.location.lower()
            jobs = [j for j in jobs if loc_lower in j.location.lower()]
        if params.job_type:
            jobs = [j for j in jobs if j.job_type == params.job_type]

        return jobs

    def get_job(self, job_id: str) -> Job | None:
        """Get a specific job by ID. Placeholder implementation."""
        return _mock_job()

    def create_job(self, data: JobCreate) -> Job:
        """Create a new job listing. Placeholder implementation."""
        return Job(
            id=uuid4(),
            title=data.title,
            company=data.company,
            location=data.location,
            description=data.description,
            requirements=data.requirements,
            salary_range=data.salary_range,
            job_type=data.job_type,
            source_url=data.source_url,
            created_at=datetime.now(tz=timezone.utc),
        )

    def match_jobs_to_profile(self, user_id: str) -> list[JobMatchScore]:
        """Match jobs to the user's profile. Placeholder implementation."""
        return [
            JobMatchScore(job_id=str(uuid4()), score=0.92),
            JobMatchScore(job_id=str(uuid4()), score=0.85),
            JobMatchScore(job_id=str(uuid4()), score=0.73),
        ]
