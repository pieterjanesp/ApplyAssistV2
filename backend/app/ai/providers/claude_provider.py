"""Anthropic Claude LLM provider implementation."""

import anthropic

from app.ai.base import LLMProvider
from app.ai.types import LLMRequest, LLMResponse
from app.config import get_settings

DEFAULT_MODEL = "claude-sonnet-4-20250514"


class ClaudeProvider(LLMProvider):
    """LLM provider backed by the Anthropic Messages API."""

    def __init__(self) -> None:
        settings = get_settings()
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion using the Anthropic Messages API.

        Maps the generic LLMRequest format to Anthropic's expected input:
        - System messages are extracted and passed as the top-level `system` param.
        - User/assistant messages are passed in the `messages` list.
        """
        model = request.model or DEFAULT_MODEL

        # Separate system messages from conversation messages
        system_parts: list[str] = []
        messages: list[dict[str, str]] = []

        for msg in request.messages:
            if msg.role == "system":
                system_parts.append(msg.content)
            else:
                messages.append({"role": msg.role, "content": msg.content})

        system_text = "\n\n".join(system_parts) if system_parts else ""

        kwargs: dict = {
            "model": model,
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
        }
        if system_text:
            kwargs["system"] = system_text

        response = await self.client.messages.create(**kwargs)

        # Extract text content from the response
        content = ""
        for block in response.content:
            if hasattr(block, "text"):
                content += block.text

        return LLMResponse(
            content=content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
            },
        )
