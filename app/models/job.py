from sqlalchemy import ForeignKey, String, Enum Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.job_analysis import JobAnalysis


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="jobs")
    job_analysis: Mapped[list["JobAnalysis"]] = relationship(
        back_populates="job"
    )  # in job analysis the field that points back to the job model is called job, so I use back_populates="job" to establish the relationship between the two models.
    company: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("applied", "interview", "offer", "rejected"),
        name="job_status",
        nullable=False,
    )
    url: Mapped[str] = mapped_column(nullable=True)
    salary_range: Mapped[str] = mapped_column(nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    applied_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
