from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.tokens import RefreshToken, Tokens
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import create_user, login_user, logout_user, refresh_token

router = APIRouter()


@router.post("/login", response_model=Tokens, status_code=200)
def login(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
):
    login_result = login_user(user, session)
    return login_result


@router.post("/register/", response_model=UserResponse, status_code=201)
def register(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    register_result = create_user(user, session)
    return register_result


@router.post("/logout", status_code=204)
def logout(refresh: RefreshToken):
    logout_user(refresh)


@router.post("/refresh/token", response_model=Tokens, status_code=200)
def refresh(refresh: RefreshToken, session: Annotated[Session, Depends(get_session)]):
    refresh_result = refresh_token(refresh, session)
    return refresh_result
