"""CV service with placeholder implementations."""

from datetime import datetime, timezone
from uuid import uuid4

from app.domains.documents.models import CV, CVItem, CVSection, SectionType
from app.domains.documents.schemas import CVAdaptRequest, CVGenerateRequest, CVOptimiseRequest


def _mock_cv(user_id: str, title: str = "Generated CV") -> CV:
    """Create a mock CV for placeholder responses."""
    now = datetime.now(tz=timezone.utc)
    return CV(
        id=uuid4(),
        user_id=user_id,
        title=title,
        sections=[
            CVSection(
                id=uuid4(),
                title="Experience",
                section_type=SectionType.EXPERIENCE,
                items=[
                    CVItem(
                        id=uuid4(),
                        content="Software Engineer at Acme Corp (2021-2024)",
                        order=0,
                    ),
                ],
                order=0,
            ),
            CVSection(
                id=uuid4(),
                title="Education",
                section_type=SectionType.EDUCATION,
                items=[
                    CVItem(
                        id=uuid4(),
                        content="BSc Computer Science, University of Example (2017-2021)",
                        order=0,
                    ),
                ],
                order=1,
            ),
            CVSection(
                id=uuid4(),
                title="Skills",
                section_type=SectionType.SKILLS,
                items=[
                    CVItem(id=uuid4(), content="Python, FastAPI, PostgreSQL", order=0),
                ],
                order=2,
            ),
        ],
        created_at=now,
        updated_at=now,
    )


class CVService:
    """Service for CV generation, adaptation, and retrieval."""

    def generate(self, user_id: str, data: CVGenerateRequest) -> CV:
        """Generate a new CV. Placeholder: returns mock structured data."""
        title = f"CV for {data.target_role}" if data.target_role else "Generated CV"
        return _mock_cv(user_id, title=title)

    def adapt(self, user_id: str, data: CVAdaptRequest) -> CV:
        """Adapt an existing CV to a job description. Placeholder implementation."""
        return _mock_cv(user_id, title="Adapted CV")

    def optimise(self, user_id: str, data: CVOptimiseRequest) -> CV:
        """Optimise an existing CV. Placeholder implementation."""
        return _mock_cv(user_id, title="Optimised CV")

    def get_cvs(self, user_id: str) -> list[CV]:
        """List all CVs for a user. Placeholder: returns a single mock CV."""
        return [_mock_cv(user_id)]

    def get_cv(self, user_id: str, cv_id: str) -> CV | None:
        """Get a specific CV by ID. Placeholder implementation."""
        cv = _mock_cv(user_id)
        return cv
