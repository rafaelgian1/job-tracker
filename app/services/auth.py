from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
)
from app.auth.token_store import store_refresh_token
from app.auth.utils import get_password_hash, verify_password
from app.models.user import User


def login_user(user, session: Session):
    db_user = session.query(User).filter(User.email == user.username).first()
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        return None

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
        return None
    session.refresh(db_user)
    return db_user
