import datetime as dt

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.job import status

status_values = [s for s in status.enums]


class JobCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    company: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=200)
    location: str | None = Field(default=None, max_length=100)
    status: str = Field(
        default="applied", pattern=f"^({'|'.join(status_values)})$"
    )  # for the regex pattern to recognize the exact status values
    url: HttpUrl | None = Field(default=None)
    salary_range: str | None = Field(default=None, max_length=50)
    notes: str | None = Field(default=None, max_length=1000)
    applied_at: dt.datetime = Field(default_factory=dt.datetime.now)


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    company: str
    title: str
    location: str | None
    status: str = Field(
        pattern=f"^({'|'.join(status_values)})$"
    )  # for the regex pattern to recognize the exact status values
    url: HttpUrl | None
    salary_range: str | None
    notes: str | None
    applied_at: dt.datetime
    updated_at: dt.datetime


class JobPatch(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    company: str | None = Field(default=None, min_length=1, max_length=100)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    location: str | None = Field(default=None, max_length=100)
    status: str | None = Field(
        default=None, pattern=f"^({'|'.join(status_values)})$"
    )  # for the regex pattern to recognize the exact status values
    url: HttpUrl | None = Field(default=None)
    salary_range: str | None = Field(default=None, max_length=50)
    notes: str | None = Field(default=None, max_length=1000)
    applied_at: dt.datetime | None = Field(default=None)
