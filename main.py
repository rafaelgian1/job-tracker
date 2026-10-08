from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.jwt_bearer import get_current_user_id
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
from app.core.database import Base, engine, get_session
from app.models.user import User
from app.schemas.refresh_token import RefreshToken
from app.schemas.tokens import Tokens
from app.schemas.user import UserCreate, UserResponse


@asynccontextmanager  # because FastAPI's lifespan function is an async context manager, we can use the @asynccontextmanager decorator to define a function that will be called when the application starts and stops.
async def lifespan(app: FastAPI):
    # Create the database tables
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
router = APIRouter()


@router.get("/users/me/", response_model=UserResponse)
def read_current_user(
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    session: Annotated[Session, Depends(get_session)],
):
    user = session.get(User, current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return user


@router.post("/register/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    db_user = User(email=user.email, hashed_password=get_password_hash(user.password))
    session.add(db_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    session.refresh(db_user)
    return db_user


@router.post("/login", response_model=Tokens, status_code=200)
def login_user(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
):
    db_user = session.query(User).filter(User.email == user.username).first()
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password!")

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


@router.post("/refresh/token", response_model=Tokens, status_code=200)
def refresh_token(
    refresh: RefreshToken,
    session: Annotated[Session, Depends(get_session)],
):
    try:
        payload = decode_token(refresh.refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload.get("type") != REFRESH:
        raise HTTPException(status_code=401, detail="Invalid token type")
    jti = payload.get("jti")
    if not is_refresh_token_active(jti):
        raise HTTPException(status_code=401, detail="Refresh token is not active")
    current_user_id = payload.get("sub")
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = session.get(User, int(current_user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    new_access_token = create_access_token(
        str(current_user_id),
        str(user.email),
    )

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/logout", status_code=204)
def logout_user(
    refresh: RefreshToken,
):
    try:
        payload = decode_token(refresh.refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload.get("type") != REFRESH:
        raise HTTPException(status_code=401, detail="Invalid token type")
    jti = payload.get("jti")
    if not is_refresh_token_active(jti):
        raise HTTPException(status_code=401, detail="Refresh token is not active")
    revoke_refresh_token(jti)


app.include_router(router)
