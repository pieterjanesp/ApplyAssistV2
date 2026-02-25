"""Profile domain API routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.domains.profile.extraction.service import SECTION_ORDER, ExtractionService
from app.domains.profile.schemas import (
    ExtractionChatRequest,
    ExtractionChatResponse,
    ExtractionFinalizeRequest,
    ExtractionFinalizeResponse,
    ExtractionSaveRequest,
    ExtractionSaveResponse,
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)
from app.domains.profile.service import ProfileService

router = APIRouter(tags=["profile"])


def _get_service() -> ProfileService:
    return ProfileService()


def _get_extraction_service() -> ExtractionService:
    return ExtractionService()


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


# --- Extraction endpoints ---


@router.post("/extract/chat", response_model=ExtractionChatResponse)
async def extraction_chat(
    data: ExtractionChatRequest,
    user_id: str = Depends(get_current_user),
    service: ExtractionService = Depends(_get_extraction_service),
) -> ExtractionChatResponse:
    """Chat with the AI interview agent for a given section."""
    if data.section not in SECTION_ORDER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid section '{data.section}'. Must be one of: {SECTION_ORDER}",
        )

    ai_message, updated_history = await service.chat(
        section=data.section,
        user_message=data.message,
        message_history=data.message_history,
        extraction_state=data.extraction_state,
        user_id=user_id,
    )

    return ExtractionChatResponse(
        ai_message=ai_message,
        message_history=updated_history,
    )


@router.post("/extract/finalize-section", response_model=ExtractionFinalizeResponse)
async def extraction_finalize_section(
    data: ExtractionFinalizeRequest,
    user_id: str = Depends(get_current_user),
    service: ExtractionService = Depends(_get_extraction_service),
) -> ExtractionFinalizeResponse:
    """Finalize a section by extracting structured data from the conversation."""
    if data.section not in SECTION_ORDER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid section '{data.section}'. Must be one of: {SECTION_ORDER}",
        )

    extracted_data, updated_state = await service.finalize_section(
        section=data.section,
        message_history=data.message_history,
        extraction_state=data.extraction_state,
        user_id=user_id,
    )

    return ExtractionFinalizeResponse(
        extracted_data=extracted_data,
        extraction_state=updated_state,
    )


@router.post("/extract/save", response_model=ExtractionSaveResponse)
async def extraction_save(
    data: ExtractionSaveRequest,
    user_id: str = Depends(get_current_user),
    profile_service: ProfileService = Depends(_get_service),
) -> ExtractionSaveResponse:
    """Save all extracted data to the database."""
    profile = profile_service.save_extraction(user_id, data.extraction_state)
    return ExtractionSaveResponse(profile=ProfileResponse(**profile))
