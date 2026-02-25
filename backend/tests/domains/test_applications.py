"""Tests for the applications domain routes."""

import pytest
from httpx import AsyncClient

AUTH_HEADERS = {"Authorization": "Bearer fake-token"}


@pytest.mark.asyncio
async def test_create_application(async_client: AsyncClient) -> None:
    """POST /api/v1/applications/ creates an application and returns 201."""
    response = await async_client.post(
        "/api/v1/applications/",
        headers=AUTH_HEADERS,
        json={"job_id": "test-job-id"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["job_id"] == "test-job-id"
    assert data["status"] == "draft"


@pytest.mark.asyncio
async def test_list_applications(async_client: AsyncClient) -> None:
    """GET /api/v1/applications/ returns a list of applications."""
    response = await async_client.get(
        "/api/v1/applications/",
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_application(async_client: AsyncClient) -> None:
    """PATCH /api/v1/applications/{id} updates the application."""
    response = await async_client.patch(
        "/api/v1/applications/some-app-id",
        headers=AUTH_HEADERS,
        json={"status": "applied"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "applied"
