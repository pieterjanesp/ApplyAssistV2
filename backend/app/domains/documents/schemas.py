"""Documents domain request/response schemas."""

from pydantic import BaseModel

from app.domains.documents.models import CoverLetter, CV


class CVGenerateRequest(BaseModel):
    """Request body for generating a new CV."""

    job_description: str | None = None
    target_role: str | None = None


class CVAdaptRequest(BaseModel):
    """Request body for adapting an existing CV to a job description."""

    cv_id: str
    job_description: str


class CVOptimiseRequest(BaseModel):
    """Request body for optimising an existing CV."""

    cv_id: str
    instructions: str | None = None


class CVResponse(CV):
    """CV response schema."""

    pass


class CoverLetterGenerateRequest(BaseModel):
    """Request body for generating a cover letter."""

    job_id: str | None = None
    job_description: str | None = None
    tone: str = "professional"


class CoverLetterResponse(CoverLetter):
    """Cover letter response schema."""

    pass
