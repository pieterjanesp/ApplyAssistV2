"""Shared FastAPI dependencies."""

from fastapi import Depends, Header, HTTPException, status

from app.ai.base import LLMProvider
from app.ai.factory import get_llm_provider as _get_llm_provider
from app.core.security import verify_jwt


async def get_current_user(authorization: str = Header(...)) -> str:
    """Extract and verify the Bearer token from the Authorization header.

    Returns the user_id string from the JWT payload.
    Raises HTTP 401 if the token is missing, malformed, or invalid.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header. Expected 'Bearer <token>'.",
        )

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing.",
        )

    payload = verify_jwt(token)
    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing 'sub' claim.",
        )

    return user_id


def get_llm_provider() -> LLMProvider:
    """Return an LLMProvider instance based on the configured AI_PROVIDER."""
    return _get_llm_provider()
