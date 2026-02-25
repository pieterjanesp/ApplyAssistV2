"""FastAPI application entry point for ApplyAssistV2."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.domains.applications.router import router as applications_router
from app.domains.documents.router import router as documents_router
from app.domains.jobs.router import router as jobs_router
from app.domains.profile.router import router as profile_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="ApplyAssistV2",
        version="0.1.0",
        description="AI-powered job application assistant API",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    register_exception_handlers(app)

    # Routers
    app.include_router(profile_router, prefix="/api/v1/profile")
    app.include_router(documents_router, prefix="/api/v1/documents")
    app.include_router(jobs_router, prefix="/api/v1/jobs")
    app.include_router(applications_router, prefix="/api/v1/applications")

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy"}

    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint returning app info."""
        return {"app": "ApplyAssistV2", "version": "0.1.0"}

    return app


app = create_app()
