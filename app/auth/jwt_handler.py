from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt

from app.core.config import settings


def create_access_token(
    subject: str, email: str, expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = expires_delta + datetime.now(timezone.utc)
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "email": str(email),
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    payoad = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return payoad
