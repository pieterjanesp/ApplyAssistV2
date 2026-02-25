"""JWT verification utilities."""

import jwt
from fastapi import HTTPException, status

from app.config import get_settings


def verify_jwt(token: str) -> dict:
    """Decode and verify a Supabase-issued JWT.

    Uses HS256 algorithm and expects the 'authenticated' audience claim.
    Returns the decoded payload dict on success.
    Raises HTTP 401 on any verification failure.
    """
    settings = get_settings()
    try:
        payload: dict = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
        )
    except jwt.InvalidAudienceError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token audience.",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )
