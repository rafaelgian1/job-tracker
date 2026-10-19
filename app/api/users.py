from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.auth.jwt_bearer import get_current_user_id
from app.core.database import get_session
from app.schemas.user import UserResponse
from app.services.users import read_current_user

router = APIRouter()


@router.get("/users/me", response_model=UserResponse)
def read_user(
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    session: Annotated[Session, Depends(get_session)],
):
    read_user_result = read_current_user(current_user_id, session)
    if read_user_result is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return read_user_result
