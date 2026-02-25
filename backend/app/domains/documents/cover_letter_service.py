"""Cover letter service with placeholder implementations."""

from datetime import datetime, timezone
from uuid import uuid4

from app.domains.documents.models import CoverLetter
from app.domains.documents.schemas import CoverLetterGenerateRequest


def _mock_cover_letter(user_id: str, tone: str = "professional") -> CoverLetter:
    """Create a mock cover letter for placeholder responses."""
    now = datetime.now(tz=timezone.utc)
    return CoverLetter(
        id=uuid4(),
        user_id=user_id,
        job_id=None,
        content=(
            "Dear Hiring Manager,\n\n"
            "I am writing to express my interest in the position at your company. "
            "With my background in software engineering and passion for building "
            "impactful products, I believe I would be a strong addition to your team.\n\n"
            "Thank you for your consideration.\n\n"
            "Best regards"
        ),
        tone=tone,
        created_at=now,
        updated_at=now,
    )


class CoverLetterService:
    """Service for cover letter generation and retrieval."""

    def generate(self, user_id: str, data: CoverLetterGenerateRequest) -> CoverLetter:
        """Generate a cover letter. Placeholder: returns mock data."""
        return _mock_cover_letter(user_id, tone=data.tone)

    def get_cover_letters(self, user_id: str) -> list[CoverLetter]:
        """List all cover letters for a user. Placeholder implementation."""
        return [_mock_cover_letter(user_id)]
