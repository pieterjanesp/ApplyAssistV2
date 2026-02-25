"""Shared pytest fixtures for backend tests."""

from collections.abc import AsyncGenerator
from unittest.mock import MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import Settings


@pytest.fixture
def mock_settings() -> Settings:
    """Return a Settings instance with test values (no real credentials)."""
    return Settings(
        SUPABASE_URL="https://test-project.supabase.co",
        SUPABASE_SERVICE_ROLE_KEY="test-service-role-key",
        SUPABASE_JWT_SECRET="test-jwt-secret-that-is-long-enough-for-hs256",
        AI_PROVIDER="claude",
        ANTHROPIC_API_KEY="test-anthropic-key",
        OPENAI_API_KEY="test-openai-key",
        CORS_ORIGINS=["http://localhost:5173"],
    )


@pytest.fixture
def mock_supabase_client() -> MagicMock:
    """Return a mock Supabase client."""
    client = MagicMock()
    # Set up common chained call patterns
    table_mock = MagicMock()
    client.table.return_value = table_mock
    table_mock.select.return_value = table_mock
    table_mock.insert.return_value = table_mock
    table_mock.update.return_value = table_mock
    table_mock.eq.return_value = table_mock
    table_mock.maybe_single.return_value = table_mock
    table_mock.execute.return_value = MagicMock(data=[])
    return client


@pytest.fixture
async def async_client(
    mock_settings: Settings,
    mock_supabase_client: MagicMock,
) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client for the FastAPI app.

    Patches settings and supabase client to avoid real external calls.
    """
    with (
        patch("app.config.get_settings", return_value=mock_settings),
        patch("app.core.supabase.get_supabase_client", return_value=mock_supabase_client),
        patch("app.core.security.get_settings", return_value=mock_settings),
        patch("app.dependencies.verify_jwt", return_value={"sub": "test-user-id"}),
    ):
        # Import app after patching so it picks up mocked settings
        from app.main import create_app

        app = create_app()
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client
