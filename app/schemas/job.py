from pydantic import BaseModel, ConfigDict, Field, HttpUrl
import datetime as dt
from typing import Literal


class JobCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    company: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=200)
    location: str | None = Field(default=None, max_length=100)
    status: Literal["applied", "interview", "offer", "rejected"] = Field(
        default="applied"
    )
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
    status: Literal["applied", "interview", "offer", "rejected"]
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
    status: Literal["applied", "interview", "offer", "rejected"] | None = Field(
        default=None
    )
    url: HttpUrl | None = Field(default=None)
    salary_range: str | None = Field(default=None, max_length=50)
    notes: str | None = Field(default=None, max_length=1000)
    applied_at: dt.datetime | None = Field(default=None)
