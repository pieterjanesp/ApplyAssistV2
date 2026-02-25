"""Shared types for the AI / LLM layer."""

from pydantic import BaseModel, Field


class Message(BaseModel):
    """A single message in a conversation."""

    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str


class LLMRequest(BaseModel):
    """Request payload for an LLM generation call."""

    messages: list[Message]
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 4096


class LLMResponse(BaseModel):
    """Response from an LLM generation call."""

    content: str
    model: str
    usage: dict[str, int] = Field(
        default_factory=lambda: {"prompt_tokens": 0, "completion_tokens": 0}
    )
