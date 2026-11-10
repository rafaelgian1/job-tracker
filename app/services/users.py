from sqlalchemy.orm import Session

from app.core.exceptions import AuthError
from app.models.user import User


def read_current_user(current_user_id, session: Session):
    user = session.get(User, current_user_id)
    if not user:
        raise AuthError(message="Invalid or expired token", error_code=401)
    return user