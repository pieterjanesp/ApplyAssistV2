"""Documents domain API routes for CVs and cover letters."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.domains.documents.cover_letter_service import CoverLetterService
from app.domains.documents.cv_service import CVService
from app.domains.documents.schemas import (
    CoverLetterGenerateRequest,
    CoverLetterResponse,
    CVAdaptRequest,
    CVGenerateRequest,
    CVOptimiseRequest,
    CVResponse,
)

router = APIRouter(tags=["documents"])


def _get_cv_service() -> CVService:
    return CVService()


def _get_cl_service() -> CoverLetterService:
    return CoverLetterService()


# ──────────────────────────────────────────────
# CV routes
# ──────────────────────────────────────────────


@router.post("/cv/generate", response_model=CVResponse, status_code=status.HTTP_201_CREATED)
async def generate_cv(
    data: CVGenerateRequest,
    user_id: str = Depends(get_current_user),
    service: CVService = Depends(_get_cv_service),
) -> CVResponse:
    """Generate a new CV, optionally tailored to a job description."""
    cv = service.generate(user_id, data)
    return CVResponse(**cv.model_dump())


@router.post("/cv/adapt", response_model=CVResponse)
async def adapt_cv(
    data: CVAdaptRequest,
    user_id: str = Depends(get_current_user),
    service: CVService = Depends(_get_cv_service),
) -> CVResponse:
    """Adapt an existing CV for a specific job description."""
    cv = service.adapt(user_id, data)
    return CVResponse(**cv.model_dump())


@router.post("/cv/optimise", response_model=CVResponse)
async def optimise_cv(
    data: CVOptimiseRequest,
    user_id: str = Depends(get_current_user),
    service: CVService = Depends(_get_cv_service),
) -> CVResponse:
    """Optimise an existing CV with optional instructions."""
    cv = service.optimise(user_id, data)
    return CVResponse(**cv.model_dump())


@router.get("/cv/", response_model=list[CVResponse])
async def list_cvs(
    user_id: str = Depends(get_current_user),
    service: CVService = Depends(_get_cv_service),
) -> list[CVResponse]:
    """List all CVs belonging to the current user."""
    cvs = service.get_cvs(user_id)
    return [CVResponse(**cv.model_dump()) for cv in cvs]


@router.get("/cv/{cv_id}", response_model=CVResponse)
async def get_cv(
    cv_id: str,
    user_id: str = Depends(get_current_user),
    service: CVService = Depends(_get_cv_service),
) -> CVResponse:
    """Get a specific CV by ID."""
    cv = service.get_cv(user_id, cv_id)
    if cv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found.",
        )
    return CVResponse(**cv.model_dump())


# ──────────────────────────────────────────────
# Cover letter routes
# ──────────────────────────────────────────────


@router.post(
    "/cover-letter/generate",
    response_model=CoverLetterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_cover_letter(
    data: CoverLetterGenerateRequest,
    user_id: str = Depends(get_current_user),
    service: CoverLetterService = Depends(_get_cl_service),
) -> CoverLetterResponse:
    """Generate a cover letter for a job."""
    cl = service.generate(user_id, data)
    return CoverLetterResponse(**cl.model_dump())


@router.get("/cover-letter/", response_model=list[CoverLetterResponse])
async def list_cover_letters(
    user_id: str = Depends(get_current_user),
    service: CoverLetterService = Depends(_get_cl_service),
) -> list[CoverLetterResponse]:
    """List all cover letters belonging to the current user."""
    letters = service.get_cover_letters(user_id)
    return [CoverLetterResponse(**cl.model_dump()) for cl in letters]
