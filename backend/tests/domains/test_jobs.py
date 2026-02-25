"""Tests for the jobs domain routes."""

import pytest
from httpx import AsyncClient

AUTH_HEADERS = {"Authorization": "Bearer fake-token"}


@pytest.mark.asyncio
async def test_list_jobs(async_client: AsyncClient) -> None:
    """GET /api/v1/jobs/ returns a list of jobs."""
    response = await async_client.get(
        "/api/v1/jobs/",
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_job(async_client: AsyncClient) -> None:
    """POST /api/v1/jobs/ creates a job and returns 201."""
    response = await async_client.post(
        "/api/v1/jobs/",
        headers=AUTH_HEADERS,
        json={
            "title": "Software Engineer",
            "company": "Test Corp",
            "location": "Remote",
            "description": "Build great things.",
            "requirements": ["Python", "FastAPI"],
            "job_type": "full-time",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Software Engineer"


@pytest.mark.asyncio
async def test_match_jobs_to_profile(async_client: AsyncClient) -> None:
    """GET /api/v1/jobs/match/profile returns match scores."""
    response = await async_client.get(
        "/api/v1/jobs/match/profile",
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "score" in data[0]
