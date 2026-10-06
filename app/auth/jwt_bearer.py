from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.auth.jwt_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid Token Type")
    except (JWTError, ValueError, TypeError):
        raise credentials_exception
    return user_id
