"""Applications domain service with placeholder implementations."""

from datetime import datetime, timezone
from uuid import uuid4

from app.domains.applications.models import Application, ApplicationStatus
from app.domains.applications.schemas import ApplicationCreate, ApplicationUpdate


def _mock_application(
    user_id: str,
    job_id: str = "mock-job-id",
    status: ApplicationStatus = ApplicationStatus.DRAFT,
) -> Application:
    """Create a mock application for placeholder responses."""
    now = datetime.now(tz=timezone.utc)
    return Application(
        id=uuid4(),
        user_id=user_id,
        job_id=job_id,
        cv_id=None,
        cover_letter_id=None,
        status=status,
        applied_at=None,
        notes=None,
        created_at=now,
        updated_at=now,
    )


class ApplicationService:
    """Service for managing job applications."""

    def create_application(self, user_id: str, data: ApplicationCreate) -> Application:
        """Create a new application.

        In a full implementation this would orchestrate CV adaptation
        and cover letter generation. Placeholder: returns mock data.
        """
        now = datetime.now(tz=timezone.utc)
        return Application(
            id=uuid4(),
            user_id=user_id,
            job_id=data.job_id,
            cv_id=data.cv_id,
            cover_letter_id=data.cover_letter_id,
            status=ApplicationStatus.DRAFT,
            applied_at=None,
            notes=data.notes,
            created_at=now,
            updated_at=now,
        )

    def get_applications(self, user_id: str) -> list[Application]:
        """List all applications for a user. Placeholder implementation."""
        return [
            _mock_application(user_id, "job-1", ApplicationStatus.DRAFT),
            _mock_application(user_id, "job-2", ApplicationStatus.APPLIED),
        ]

    def get_application(self, user_id: str, application_id: str) -> Application | None:
        """Get a specific application by ID. Placeholder implementation."""
        return _mock_application(user_id)

    def update_application(
        self, user_id: str, application_id: str, data: ApplicationUpdate
    ) -> Application | None:
        """Update an application's status or notes. Placeholder implementation."""
        app = _mock_application(user_id)
        if data.status is not None:
            app.status = data.status
        if data.notes is not None:
            app.notes = data.notes
        app.updated_at = datetime.now(tz=timezone.utc)
        return app
