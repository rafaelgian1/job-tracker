from sqlmodel import Session

from app.models.user import User


def read_current_user(current_user_id, session: Session):
    user = session.get(User, current_user_id)
    if not user:
        return None
    return user