"""AI / LLM layer for ApplyAssistV2."""

from app.ai.base import LLMProvider
from app.ai.factory import get_llm_provider

__all__ = ["LLMProvider", "get_llm_provider"]
