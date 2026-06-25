from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)
    role: Literal["admin", "member", "viewer"] = "member"

class UserLogin(BaseModel):
    email: EmailStr
    password: str