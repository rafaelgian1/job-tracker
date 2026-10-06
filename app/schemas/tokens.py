from pydantic import BaseModel, Field


class Tokens(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = Field(default=None)