from pydantic import BaseModel, ConfigDict, Field
import datetime as dt
from typing import Literal


class JobAnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    required_skills: list[str] | None
    nice_skills: list[str] | None
    match_score: float | None = Field(
        ge=0.0, le=100.0
    )  # Ensure match_score is between 0 and 100
    analyzed_at: dt.datetime | None
    job_id: int
    analysis_status: Literal["pending", "completed", "failed"]
