"""Tests for the profile domain routes."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

AUTH_HEADERS = {"Authorization": "Bearer fake-token"}


@pytest.mark.asyncio
async def test_get_profile_not_found(async_client: AsyncClient) -> None:
    """GET /api/v1/profile/ returns 404 when no profile exists."""
    with patch.object(
        __import__("app.domains.profile.service", fromlist=["ProfileService"]).ProfileService,
        "get_profile",
        return_value=None,
    ):
        response = await async_client.get("/api/v1/profile/", headers=AUTH_HEADERS)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_profile(async_client: AsyncClient) -> None:
    """POST /api/v1/profile/ accepts valid profile data."""
    profile_data = {
        "id": "00000000-0000-0000-0000-000000000001",
        "user_id": "test-user-id",
        "full_name": "Test User",
        "email": "test@example.com",
        "phone": None,
        "location": None,
        "summary": None,
        "skills": ["Python", "FastAPI"],
        "experience_years": None,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }

    with (
        patch.object(
            __import__("app.domains.profile.service", fromlist=["ProfileService"]).ProfileService,
            "get_profile",
            return_value=None,
        ),
        patch.object(
            __import__("app.domains.profile.service", fromlist=["ProfileService"]).ProfileService,
            "create_profile",
            return_value=profile_data,
        ),
    ):
        response = await async_client.post(
            "/api/v1/profile/",
            headers=AUTH_HEADERS,
            json={
                "full_name": "Test User",
                "email": "test@example.com",
                "skills": ["Python", "FastAPI"],
            },
        )
    assert response.status_code == 201
    assert response.json()["full_name"] == "Test User"


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient) -> None:
    """GET /health returns 200 with healthy status."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient) -> None:
    """GET / returns app name and version."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "ApplyAssistV2"
    assert data["version"] == "0.1.0"


# --- Extraction endpoint tests ---


@pytest.mark.asyncio
async def test_extraction_chat_invalid_section(async_client: AsyncClient) -> None:
    """POST /extract/chat returns 400 for an invalid section name."""
    response = await async_client.post(
        "/api/v1/profile/extract/chat",
        headers=AUTH_HEADERS,
        json={
            "section": "invalid_section",
            "message": "Hello",
        },
    )
    assert response.status_code == 400
    assert "Invalid section" in response.json()["detail"]


@pytest.mark.asyncio
async def test_extraction_chat_success(async_client: AsyncClient) -> None:
    """POST /extract/chat returns an AI message when the service is mocked."""
    mock_result = (
        "Tell me about your most recent role.",
        [
            {"role": "user", "content": "Hi, I want to add my work experience"},
            {"role": "assistant", "content": "Tell me about your most recent role."},
        ],
    )

    with patch(
        "app.domains.profile.extraction.service.ExtractionService.chat",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await async_client.post(
            "/api/v1/profile/extract/chat",
            headers=AUTH_HEADERS,
            json={
                "section": "work_experience",
                "message": "Hi, I want to add my work experience",
                "message_history": [],
                "extraction_state": {},
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["ai_message"] == "Tell me about your most recent role."
    assert len(data["message_history"]) == 2


@pytest.mark.asyncio
async def test_extraction_finalize_section_invalid(async_client: AsyncClient) -> None:
    """POST /extract/finalize-section returns 400 for an invalid section."""
    response = await async_client.post(
        "/api/v1/profile/extract/finalize-section",
        headers=AUTH_HEADERS,
        json={
            "section": "bad_section",
            "message_history": [],
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_extraction_finalize_section_success(async_client: AsyncClient) -> None:
    """POST /extract/finalize-section returns extracted data when mocked."""
    extracted_data = {
        "items": [
            {
                "job_title": "Software Engineer",
                "company": "Acme Corp",
                "is_current": True,
            }
        ]
    }
    updated_state = {
        "work_experiences": [
            {
                "job_title": "Software Engineer",
                "company": "Acme Corp",
                "is_current": True,
            }
        ],
    }
    mock_result = (extracted_data, updated_state)

    with patch(
        "app.domains.profile.extraction.service.ExtractionService.finalize_section",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await async_client.post(
            "/api/v1/profile/extract/finalize-section",
            headers=AUTH_HEADERS,
            json={
                "section": "work_experience",
                "message_history": [
                    {"role": "user", "content": "I work at Acme Corp as a Software Engineer"},
                    {"role": "assistant", "content": "Got it!"},
                ],
                "extraction_state": {},
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert "extracted_data" in data
    assert "extraction_state" in data
    assert data["extracted_data"]["items"][0]["job_title"] == "Software Engineer"


@pytest.mark.asyncio
async def test_extraction_save(async_client: AsyncClient) -> None:
    """POST /extract/save persists extraction state and returns profile."""
    profile_row = {
        "id": "00000000-0000-0000-0000-000000000001",
        "user_id": "test-user-id",
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "phone": None,
        "location": "London",
        "summary": None,
        "skills": ["Python", "FastAPI"],
        "experience_years": None,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }

    with patch.object(
        __import__("app.domains.profile.service", fromlist=["ProfileService"]).ProfileService,
        "save_extraction",
        return_value=profile_row,
    ):
        response = await async_client.post(
            "/api/v1/profile/extract/save",
            headers=AUTH_HEADERS,
            json={
                "extraction_state": {
                    "basic_info": {
                        "full_name": "Jane Doe",
                        "email": "jane@example.com",
                        "location": "London",
                    },
                    "work_experiences": [
                        {
                            "job_title": "Software Engineer",
                            "company": "Acme Corp",
                            "is_current": True,
                        }
                    ],
                    "education": [],
                    "skills": ["Python", "FastAPI"],
                    "career_goals": None,
                }
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["profile"]["full_name"] == "Jane Doe"
    assert data["profile"]["email"] == "jane@example.com"
