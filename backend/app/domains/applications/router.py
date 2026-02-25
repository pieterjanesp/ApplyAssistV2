"""Applications domain API routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.domains.applications.schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from app.domains.applications.service import ApplicationService

router = APIRouter(tags=["applications"])


def _get_service() -> ApplicationService:
    return ApplicationService()


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    data: ApplicationCreate,
    user_id: str = Depends(get_current_user),
    service: ApplicationService = Depends(_get_service),
) -> ApplicationResponse:
    """Create a new application (orchestrates CV adapt + cover letter generation)."""
    application = service.create_application(user_id, data)
    return ApplicationResponse(**application.model_dump())


@router.get("/", response_model=list[ApplicationResponse])
async def list_applications(
    user_id: str = Depends(get_current_user),
    service: ApplicationService = Depends(_get_service),
) -> list[ApplicationResponse]:
    """List all applications for the current user."""
    applications = service.get_applications(user_id)
    return [ApplicationResponse(**a.model_dump()) for a in applications]


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: str,
    user_id: str = Depends(get_current_user),
    service: ApplicationService = Depends(_get_service),
) -> ApplicationResponse:
    """Get a specific application by ID."""
    application = service.get_application(user_id, application_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )
    return ApplicationResponse(**application.model_dump())


@router.patch("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: str,
    data: ApplicationUpdate,
    user_id: str = Depends(get_current_user),
    service: ApplicationService = Depends(_get_service),
) -> ApplicationResponse:
    """Update an application's status or notes."""
    application = service.update_application(user_id, application_id, data)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )
    return ApplicationResponse(**application.model_dump())
