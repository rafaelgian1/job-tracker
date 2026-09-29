from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.jwt_bearer import get_current_user_id
from app.auth.jwt_handler import create_access_token
from app.auth.utils import get_password_hash, verify_password
from app.core.config import settings
from app.core.database import Base, engine, get_session
from app.models.user import User
from app.schemas.token import Token
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


@router.get("/users/{user_id}/", response_model=UserResponse)
def read_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return user


@router.post("/login", response_model=Token, status_code=200)
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
    return {"access_token": access_token, "token_type": "bearer"}


app.include_router(router)
