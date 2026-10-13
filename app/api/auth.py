from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.tokens import Tokens
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import create_user, login_user

router = APIRouter()


@router.post("/login", response_model=Tokens, status_code=200)
def login(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
):
    login_result = login_user(user, session)
    if login_result is None:
        raise HTTPException(status_code=401, detail="Invalid email or password!")
    else:
        return login_result


@router.post("/register/", response_model=UserResponse, status_code=201)
def register(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    register_result = create_user(user, session)
    if register_result is None:
        raise HTTPException(status_code=409, detail="Email already registered")
    else:
        return register_result
