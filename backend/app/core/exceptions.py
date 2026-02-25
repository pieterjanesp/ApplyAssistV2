"""Custom application exceptions and FastAPI exception handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str = "An application error occurred.") -> None:
        self.message = message
        super().__init__(self.message)


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found.") -> None:
        super().__init__(message)


class ForbiddenError(AppError):
    """Raised when the user lacks permission for the requested action."""

    def __init__(self, message: str = "Forbidden.") -> None:
        super().__init__(message)


class BadRequestError(AppError):
    """Raised when the request is malformed or contains invalid data."""

    def __init__(self, message: str = "Bad request.") -> None:
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on the FastAPI application."""

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message},
        )

    @app.exception_handler(ForbiddenError)
    async def forbidden_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
        return JSONResponse(
            status_code=403,
            content={"detail": exc.message},
        )

    @app.exception_handler(BadRequestError)
    async def bad_request_handler(request: Request, exc: BadRequestError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )
