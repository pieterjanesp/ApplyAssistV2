"""Shared dependency context for extraction agents."""

from dataclasses import dataclass

from app.domains.profile.schemas import ExtractionState


@dataclass
class ExtractionContext:
    """Dependency injected into Pydantic AI agents during extraction."""

    user_id: str
    extracted_so_far: ExtractionState
    section_name: str
