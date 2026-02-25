"""Profile domain request/response schemas."""

from pydantic import BaseModel

from app.domains.profile.models import UserProfile

# --- Profile CRUD schemas ---


class ProfileCreate(BaseModel):
    """Schema for creating a new profile."""

    full_name: str
    email: str
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    skills: list[str] = []
    experience_years: int | None = None


class ProfileUpdate(BaseModel):
    """Schema for updating an existing profile. All fields are optional."""

    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    skills: list[str] | None = None
    experience_years: int | None = None


class ProfileResponse(UserProfile):
    """Profile response schema."""

    pass


# --- Extraction Create schemas (also used as Pydantic AI output types) ---


class WorkExperienceCreate(BaseModel):
    """Schema for creating a work experience record."""

    job_title: str
    company: str
    start_date: str | None = None
    end_date: str | None = None
    is_current: bool = False
    description: str | None = None
    achievements: list[str] = []
    technologies: list[str] = []


class EducationCreate(BaseModel):
    """Schema for creating an education record."""

    institution: str
    degree: str
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None


class CareerGoalsCreate(BaseModel):
    """Schema for creating career goals."""

    target_roles: list[str] = []
    target_industries: list[str] = []
    career_narrative: str | None = None
    motivations: str | None = None
    preferred_work_style: str | None = None


# --- Extraction agent output wrappers ---


class WorkExperienceExtracted(BaseModel):
    """Extraction agent output: list of work experiences."""

    items: list[WorkExperienceCreate]


class EducationExtracted(BaseModel):
    """Extraction agent output: list of education records."""

    items: list[EducationCreate]


class SkillsExtracted(BaseModel):
    """Extraction agent output: list of skills."""

    skills: list[str]


# --- Extraction state & API schemas ---


class ExtractionState(BaseModel):
    """Accumulated structured data across all completed sections."""

    basic_info: ProfileCreate | None = None
    work_experiences: list[WorkExperienceCreate] = []
    education: list[EducationCreate] = []
    skills: list[str] = []
    career_goals: CareerGoalsCreate | None = None


class ChatMessage(BaseModel):
    """A single message in the extraction conversation."""

    role: str  # "user" or "assistant"
    content: str


class ExtractionChatRequest(BaseModel):
    """Request schema for the extraction chat endpoint."""

    section: str
    message: str
    message_history: list[ChatMessage] = []
    extraction_state: ExtractionState = ExtractionState()


class ExtractionChatResponse(BaseModel):
    """Response schema for the extraction chat endpoint."""

    ai_message: str
    message_history: list[ChatMessage]


class ExtractionFinalizeRequest(BaseModel):
    """Request schema for the finalize-section endpoint."""

    section: str
    message_history: list[ChatMessage]
    extraction_state: ExtractionState = ExtractionState()


class ExtractionFinalizeResponse(BaseModel):
    """Response schema for the finalize-section endpoint."""

    extracted_data: dict
    extraction_state: ExtractionState


class ExtractionSaveRequest(BaseModel):
    """Request schema for the save endpoint."""

    extraction_state: ExtractionState


class ExtractionSaveResponse(BaseModel):
    """Response schema for the save endpoint."""

    profile: ProfileResponse
