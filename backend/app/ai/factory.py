"""Factory for creating LLM provider instances."""

from app.ai.base import LLMProvider
from app.config import get_settings


def get_llm_provider(provider: str | None = None) -> LLMProvider:
    """Return the appropriate LLM provider instance.

    Args:
        provider: Provider name ("claude" or "openai"). If None, reads
                  from the AI_PROVIDER setting.

    Returns:
        An LLMProvider instance.

    Raises:
        ValueError: If the provider name is not recognised.
    """
    if provider is None:
        provider = get_settings().AI_PROVIDER

    provider = provider.lower().strip()

    if provider == "claude":
        from app.ai.providers.claude_provider import ClaudeProvider

        return ClaudeProvider()
    elif provider == "openai":
        from app.ai.providers.openai_provider import OpenAIProvider

        return OpenAIProvider()
    else:
        raise ValueError(
            f"Unknown AI provider '{provider}'. Supported providers: claude, openai."
        )
