from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.cv import Cv

if TYPE_CHECKING:
    from app.models.job import Job


class JobAnalysis(Base):
    __tablename__ = "job_analysis"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    job: Mapped["Job"] = relationship(back_populates="job_analysis")
    cv_id: Mapped[int] = mapped_column(ForeignKey("cvs.id"))
    cv: Mapped["Cv"] = relationship(back_populates="job_analysis")
    required_skills: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    nice_skills: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    match_score: Mapped[float] = mapped_column(nullable=True)
    analyzed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    analysis_status: Mapped[str] = mapped_column(
        Enum("completed", "failed", name="analysis_status"),
        nullable=False,
        default="completed",
    )
