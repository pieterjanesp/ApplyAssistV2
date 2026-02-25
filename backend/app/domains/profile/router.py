"""Profile domain API routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.domains.profile.schemas import ProfileCreate, ProfileResponse, ProfileUpdate
from app.domains.profile.service import ProfileService

router = APIRouter(tags=["profile"])


def _get_service() -> ProfileService:
    return ProfileService()


@router.get("/", response_model=ProfileResponse)
async def get_profile(
    user_id: str = Depends(get_current_user),
    service: ProfileService = Depends(_get_service),
) -> ProfileResponse:
    """Get the current user's profile."""
    profile = service.get_profile(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )
    return ProfileResponse(**profile)


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    data: ProfileCreate,
    user_id: str = Depends(get_current_user),
    service: ProfileService = Depends(_get_service),
) -> ProfileResponse:
    """Create a new profile for the current user."""
    existing = service.get_profile(user_id)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists.",
        )
    profile = service.create_profile(user_id, data)
    return ProfileResponse(**profile)


@router.patch("/", response_model=ProfileResponse)
async def update_profile(
    data: ProfileUpdate,
    user_id: str = Depends(get_current_user),
    service: ProfileService = Depends(_get_service),
) -> ProfileResponse:
    """Update the current user's profile."""
    profile = service.update_profile(user_id, data)
    return ProfileResponse(**profile)


@router.post("/extract", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def extract_profile_info(
    user_id: str = Depends(get_current_user),
) -> dict[str, str]:
    """Extract profile information from uploaded documents (not yet implemented)."""
    return {"detail": "Profile extraction is not yet implemented."}
