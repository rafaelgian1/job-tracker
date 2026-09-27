from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.utils import get_password_hash, verify_password
from app.core.database import Base, engine, get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


@asynccontextmanager  # because FastAPI's lifespan function is an async context manager, we can use the @asynccontextmanager decorator to define a function that will be called when the application starts and stops.
async def lifespan(app: FastAPI):
    # Create the database tables
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/token/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


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


app.include_router(router)
