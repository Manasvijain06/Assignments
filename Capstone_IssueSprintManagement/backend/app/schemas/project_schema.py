from pydantic import BaseModel, EmailStr, Field
from typing import List


class ProjectCreate(BaseModel):
    name: str = Field(min_length=3)
    description: str
    project_key: str = Field(min_length=2)
    members: List[EmailStr] = []


class ProjectResponse(BaseModel):
    message: str
    project_id: str


class ProjectMemberRequest(BaseModel):
    admin_email: EmailStr
    member_email: EmailStr


class ProjectMemberResponse(BaseModel):
    message: str

class UserListResponse(BaseModel):
    name: str
    email: EmailStr
    role: str

class ProjectUpdate(BaseModel):
    name: str = Field(min_length=3)
    description: str
    project_key: str = Field(min_length=2)


class ProjectListResponse(BaseModel):
    project_id: str
    name: str
    description: str
    project_key: str
    members: List[EmailStr]
    created_by: str