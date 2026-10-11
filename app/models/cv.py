from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


# importing the Base from database file to use it as the base class for the model.

if TYPE_CHECKING:
    from app.models.job_analysis import JobAnalysis
    from app.models.user import User

class Cv(Base):
    __tablename__ = "cvs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="cvs")
    raw_text: Mapped[str] = mapped_column(nullable=False)
    extracted_skills: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.now)
    job_analysis: Mapped[list["JobAnalysis"]] = relationship(
            back_populates="cv")
