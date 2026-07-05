import base64
import re
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    """
    Request schema for user registration."""
    name: str
    email: EmailStr
    password: str = Field(description="Base64-encoded password")
    role: Literal["admin", "member", "viewer"]

    @field_validator("email")
    def validate_email(cls, email: EmailStr):
        """
        Validate email format.
        """
        if not str(email).endswith("@gmail.com"):
            raise ValueError("Invalid email format")
        return email

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        """
        Validate decoded password strength.
        """
        try:
            decoded_password = base64.b64decode(password).decode("utf-8")
        except Exception:
            raise ValueError("Invalid password encoding")

        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*]).{6,}$"

        if not re.match(pattern, decoded_password):
            raise ValueError(
                "Password must be at least 6 characters and include uppercase, lowercase, digit, and special character."
            )

        return password

class UserLoginRequest(BaseModel):
    """
    User login request schema.
    """

    email: EmailStr
    password: str = Field(description="Base64-encoded password")