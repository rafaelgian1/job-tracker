from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)
import datetime as dt


class UserCreate(BaseModel):
    password: str = Field(..., min_length=8)
    email: EmailStr  # Validate email format


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    created_at: dt.datetime
    email: EmailStr


class UserPatch(BaseModel):
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

    current_password: str | None = Field(min_length=8, default=None)
    new_password: str | None = Field(
        min_length=8, default=None
    )  # Validate that both current_password and new_password are provided together

    @field_validator("email", mode="before")
    def clean_email(cls, v):
        if v is not None:
            return v.strip()  # Strip whitespace from email
        return v

    email: EmailStr | None = Field(default=None)  # Validate email format
