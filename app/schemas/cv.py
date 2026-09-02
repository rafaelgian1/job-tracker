from pydantic import BaseModel, ConfigDict, Field
import datetime as dt
from typing import Literal


class CVResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    uploaded_at: dt.datetime
    extracted_skills: list[
        str
    ]  # The list of skills extracted from the CV, if no skills were extracted, this will be an empty list
    status: Literal["pending", "processed", "failed"]
    # The status of the CV processing"
