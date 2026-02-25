"""Extraction orchestration service."""

from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart

from app.domains.profile.extraction.agents import (
    DEFAULT_MODEL,
    EXTRACTION_AGENTS,
    INTERVIEW_AGENTS,
)
from app.domains.profile.extraction.deps import ExtractionContext
from app.domains.profile.schemas import (
    CareerGoalsCreate,
    ChatMessage,
    EducationExtracted,
    ExtractionState,
    SkillsExtracted,
    WorkExperienceExtracted,
)

SECTION_ORDER = ["work_experience", "education", "skills", "career_goals"]


def _chat_to_model_messages(history: list[ChatMessage]) -> list[ModelMessage]:
    """Convert our ChatMessage list to pydantic-ai ModelMessage list."""
    messages: list[ModelMessage] = []
    for msg in history:
        if msg.role == "user":
            messages.append(ModelRequest(parts=[UserPromptPart(content=msg.content)]))
        elif msg.role == "assistant":
            messages.append(ModelResponse(parts=[TextPart(content=msg.content)]))
    return messages


def _model_messages_to_chat(messages: list[ModelMessage]) -> list[ChatMessage]:
    """Convert pydantic-ai ModelMessage list back to our ChatMessage list.

    Only extracts user and assistant text messages (skips system, tool calls, etc.).
    """
    result: list[ChatMessage] = []
    for msg in messages:
        if isinstance(msg, ModelRequest):
            for part in msg.parts:
                if isinstance(part, UserPromptPart) and isinstance(part.content, str):
                    result.append(ChatMessage(role="user", content=part.content))
        elif isinstance(msg, ModelResponse):
            for part in msg.parts:
                if isinstance(part, TextPart):
                    result.append(ChatMessage(role="assistant", content=part.content))
    return result


class ExtractionService:
    """Orchestrates the extraction interview flow."""

    async def chat(
        self,
        section: str,
        user_message: str,
        message_history: list[ChatMessage],
        extraction_state: ExtractionState,
        user_id: str,
    ) -> tuple[str, list[ChatMessage]]:
        """Send a message to the interview agent and get a reply.

        Returns (ai_reply, updated_message_history).
        """
        agent = INTERVIEW_AGENTS[section]
        deps = ExtractionContext(
            user_id=user_id,
            extracted_so_far=extraction_state,
            section_name=section,
        )

        model_history = _chat_to_model_messages(message_history)

        result = await agent.run(
            user_message,
            message_history=model_history,
            deps=deps,
            model=DEFAULT_MODEL,
        )

        ai_reply = result.output
        updated_history = _model_messages_to_chat(result.all_messages())
        return ai_reply, updated_history

    async def finalize_section(
        self,
        section: str,
        message_history: list[ChatMessage],
        extraction_state: ExtractionState,
        user_id: str,
    ) -> tuple[dict, ExtractionState]:
        """Run the extraction agent to produce structured data from the conversation.

        Returns (extracted_data_dict, updated_extraction_state).
        """
        agent = EXTRACTION_AGENTS[section]
        deps = ExtractionContext(
            user_id=user_id,
            extracted_so_far=extraction_state,
            section_name=section,
        )

        # Build conversation transcript for the extraction agent
        transcript_parts = []
        for msg in message_history:
            role = "User" if msg.role == "user" else "Assistant"
            transcript_parts.append(f"{role}: {msg.content}")
        transcript = "\n\n".join(transcript_parts)

        result = await agent.run(
            f"Extract structured data from this conversation:\n\n{transcript}",
            deps=deps,
            model=DEFAULT_MODEL,
        )

        extracted = result.output

        # Update extraction state based on section
        new_state = extraction_state.model_copy()
        if section == "work_experience" and isinstance(extracted, WorkExperienceExtracted):
            new_state.work_experiences = extracted.items
            extracted_dict = extracted.model_dump()
        elif section == "education" and isinstance(extracted, EducationExtracted):
            new_state.education = extracted.items
            extracted_dict = extracted.model_dump()
        elif section == "skills" and isinstance(extracted, SkillsExtracted):
            new_state.skills = extracted.skills
            extracted_dict = extracted.model_dump()
        elif section == "career_goals" and isinstance(extracted, CareerGoalsCreate):
            new_state.career_goals = extracted
            extracted_dict = extracted.model_dump()
        else:
            extracted_dict = extracted.model_dump() if hasattr(extracted, "model_dump") else {}

        return extracted_dict, new_state
