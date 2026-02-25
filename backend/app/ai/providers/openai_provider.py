"""OpenAI LLM provider implementation."""

import openai

from app.ai.base import LLMProvider
from app.ai.types import LLMRequest, LLMResponse
from app.config import get_settings

DEFAULT_MODEL = "gpt-4o"


class OpenAIProvider(LLMProvider):
    """LLM provider backed by the OpenAI Chat Completions API."""

    def __init__(self) -> None:
        settings = get_settings()
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion using the OpenAI Chat Completions API.

        Maps the generic LLMRequest format directly to OpenAI's messages list.
        """
        model = request.model or DEFAULT_MODEL

        messages: list[dict[str, str]] = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore[arg-type]
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        choice = response.choices[0]
        content = choice.message.content or ""

        usage = response.usage
        usage_dict = {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
        }

        return LLMResponse(
            content=content,
            model=response.model,
            usage=usage_dict,
        )
