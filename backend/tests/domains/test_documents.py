"""Tests for the documents domain routes."""

import pytest
from httpx import AsyncClient

AUTH_HEADERS = {"Authorization": "Bearer fake-token"}


@pytest.mark.asyncio
async def test_generate_cv(async_client: AsyncClient) -> None:
    """POST /api/v1/documents/cv/generate returns 201 with CV data."""
    response = await async_client.post(
        "/api/v1/documents/cv/generate",
        headers=AUTH_HEADERS,
        json={"target_role": "Backend Developer"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "sections" in data
    assert "id" in data


@pytest.mark.asyncio
async def test_list_cvs(async_client: AsyncClient) -> None:
    """GET /api/v1/documents/cv/ returns a list of CVs."""
    response = await async_client.get(
        "/api/v1/documents/cv/",
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_generate_cover_letter(async_client: AsyncClient) -> None:
    """POST /api/v1/documents/cover-letter/generate returns 201."""
    response = await async_client.post(
        "/api/v1/documents/cover-letter/generate",
        headers=AUTH_HEADERS,
        json={"tone": "enthusiastic"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "content" in data


@pytest.mark.asyncio
async def test_list_cover_letters(async_client: AsyncClient) -> None:
    """GET /api/v1/documents/cover-letter/ returns a list of cover letters."""
    response = await async_client.get(
        "/api/v1/documents/cover-letter/",
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
