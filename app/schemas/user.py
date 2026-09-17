import datetime as dt
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from app.auth.utils import is_password_valid


def validate_password_length(password: str) -> str:
    if not is_password_valid(password):
        raise ValueError(
            "Password must be between 8 and 72 bytes in length when encoded in UTF-8."
        )
    return password


valid_byte_length = Annotated[str, AfterValidator(validate_password_length)]


class UserCreate(BaseModel):
    password: valid_byte_length
    email: EmailStr  # Validate email format


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    created_at: dt.datetime
    email: EmailStr


class UserPatch(BaseModel):
    current_password: valid_byte_length | None = Field(default=None)
    new_password: valid_byte_length | None = Field(default=None)

    @model_validator(mode="before")
    def check_passwords(cls, values):
        current_password = values.get("current_password")
        new_password = values.get("new_password")
        if (current_password and not new_password) or (
            new_password and not current_password
        ):
            raise ValueError(
                "Both current_password and new_password must be provided together."
            )
        return values

    @field_validator("email", mode="before")
    def clean_email(cls, v):
        if v is not None:
            return v.strip()  # Strip whitespace from email
        return v

    email: EmailStr | None = Field(default=None)  # Validate email format
