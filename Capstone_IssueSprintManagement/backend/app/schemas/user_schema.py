import base64
import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(description="Base64-encoded password")
    role: Literal["admin", "member", "viewer"] = "member"

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
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


class UserRegisterResponse(BaseModel):
    message: str
    user_id: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(description="Base64-encoded password")

class UserLoginResponse(BaseModel):
    message: str
    user_id: str
    name: str
    email: EmailStr
    role: str