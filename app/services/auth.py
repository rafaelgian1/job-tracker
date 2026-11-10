from jose import JWTError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    REFRESH,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.auth.token_store import (
    is_refresh_token_active,
    revoke_refresh_token,
    store_refresh_token,
)
from app.auth.utils import get_password_hash, verify_password
from app.core.exceptions import AuthError
from app.models.user import User


def login_user(user, session: Session):
    db_user = session.query(User).filter(User.email == user.username).first()
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise AuthError(message="Invalid email or password!", error_code=401)

    access_token = create_access_token(
        str(db_user.id),
        db_user.email,
    )
    refresh_token, jti = create_refresh_token(
        str(db_user.id),
    )
    store_refresh_token(jti, db_user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def create_user(user, session: Session):
    db_user = User(email=user.email, hashed_password=get_password_hash(user.password))
    session.add(db_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise AuthError(message="Email already registered", error_code=409)
    session.refresh(db_user)
    return db_user


def logout_user(refresh):
    try:
        payload = decode_token(refresh.refresh_token)
    except JWTError:
        raise AuthError(message="Invalid or expired token", error_code=401)
    if payload.get("type") != REFRESH:
        raise AuthError(message="Invalid token type", error_code=401)
    jti = payload.get("jti")
    if not is_refresh_token_active(jti):
        raise AuthError(message="Invalid or expired token", error_code=401)
    revoke_refresh_token(jti)
    return True


def refresh_token(refresh, session: Session):
    try:
        payload = decode_token(refresh.refresh_token)
    except JWTError:
        raise AuthError(message="Invalid or expired token", error_code=401)
    if payload.get("type") != REFRESH:
        raise AuthError(message="Invalid token type", error_code=401)
    jti = payload.get("jti")

    if not is_refresh_token_active(jti):
        raise AuthError(message="Invalid or expired token", error_code=401)
    current_user_id = payload.get("sub")
    if not current_user_id:
        raise AuthError(message="Invalid user ID", error_code=401)
    user = session.get(User, int(current_user_id))
    if not user:
        raise AuthError(message="User not found", error_code=404)
    new_access_token = create_access_token(
        str(current_user_id),
        str(user.email),
    )
    return {"access_token": new_access_token, "token_type": "bearer"}
