"""..."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """..."""

    email: EmailStr
    password: str = Field(min_length=8)
