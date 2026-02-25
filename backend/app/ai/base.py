"""Abstract base class for LLM providers."""

import json
from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from app.ai.types import LLMRequest, LLMResponse

T = TypeVar("T", bound=BaseModel)


class LLMProvider(ABC):
    """Abstract interface for language model providers."""

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion from the LLM.

        Args:
            request: The LLM request with messages, model, and parameters.

        Returns:
            An LLMResponse with the generated content, model name, and usage stats.
        """
        ...

    async def generate_structured(
        self, request: LLMRequest, response_model: type[T]
    ) -> T:
        """Generate a completion and parse the result into a Pydantic model.

        The LLM is expected to return valid JSON matching the response_model schema.
        A system message with the JSON schema is prepended to guide the model.

        Args:
            request: The LLM request.
            response_model: The Pydantic model class to parse the response into.

        Returns:
            An instance of response_model populated from the LLM's JSON output.
        """
        from app.ai.types import Message

        schema_json = json.dumps(response_model.model_json_schema(), indent=2)
        schema_message = Message(
            role="system",
            content=(
                "You must respond with valid JSON that conforms to the following schema. "
                "Do not include any other text outside the JSON object.\n\n"
                f"```json\n{schema_json}\n```"
            ),
        )

        augmented_request = LLMRequest(
            messages=[schema_message, *request.messages],
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        response = await self.generate(augmented_request)

        # Strip markdown code fences if present
        content = response.content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            # Remove first and last lines (the fences)
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines)

        parsed = response_model.model_validate_json(content)
        return parsed
