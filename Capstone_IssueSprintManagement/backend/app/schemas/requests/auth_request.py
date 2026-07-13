import re
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    """
    Request schema for user registration.
    """
    name: str
    email: EmailStr
    password: str
    role: Literal["admin", "member", "viewer"]

    @field_validator("email")
    def validate_email(cls, email: EmailStr):
        """
        Validate email format.
        """
        if not str(email).endswith("@gmail.com"):
            raise ValueError("Please enter a valid Gmail address.")
        return email

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        """
        Validate decoded password strength.
        """

        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*]).{6,}$"

        if not re.match(pattern, password):
            raise ValueError(
                "Password must be at least 6 characters and include"
                "uppercase, lowercase, digit, and special character."
            )

        return password

class UserLoginRequest(BaseModel):
    """
    User login request schema.
    """

    email: EmailStr
    password: str = Field(description="Plain password")