import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt

from app.core.config import settings

ACCESS = "access"
REFRESH = "refresh"


def create_access_token(subject: str, email: str) -> str:
    expire_access_token = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token_to_encode = {
        "sub": str(subject),
        "iat": datetime.now(timezone.utc),
        "email": str(email),
        "exp": expire_access_token,
        "type": ACCESS,
    }
    encoded_access_token = jwt.encode(
        access_token_to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_access_token


def create_refresh_token(subject: str):
    expire_refresh_token = datetime.now(timezone.utc) + timedelta(
        minutes=settings.refresh_token_expire_minutes
    )
    jti = str(uuid.uuid4())
    refresh_token_to_encode = {
        "sub": str(subject),
        "iat": datetime.now(timezone.utc),
        "jti": jti,
        "exp": expire_refresh_token,
        "type": REFRESH,
    }
    encoded_refresh_token = jwt.encode(
        refresh_token_to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_refresh_token, jti


def decode_token(token: str) -> dict[str, Any]:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return payload
