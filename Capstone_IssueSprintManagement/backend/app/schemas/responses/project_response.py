from typing import List, Optional

from pydantic import BaseModel, EmailStr
from app.schemas.responses.auth_response import UserResponse


class CreateProjectResponse(BaseModel):
    """
    Response schema after creating a project.
    """

    message: str
    project_id: str


class UpdateProjectResponse(BaseModel):
    """
    Response schema after updating a project.
    """

    message: str


class DeleteProjectResponse(BaseModel):
    """
    Response schema after deleting a project.
    """
    message: str


class ProjectMemberResponse(BaseModel):
    """
    Response returned after adding or removing a project member.
    """
    message: str


class ProjectCreatorResponse(BaseModel):
    """
    Project creator details.
    """

    user_id: str
    name: str
    email: EmailStr


class ProjectDetailResponse(BaseModel):
    """
    Response schema for project details.
    """

    project_id: str
    name: str
    description: str
    project_key: str
    members: List[UserResponse]
    created_by: Optional[ProjectCreatorResponse]

class ProjectListResponse(BaseModel):
    """
    Paginated response for project listing.
    """
    items: List[ProjectDetailResponse]
    page: int
    limit: int
    total: int
    total_pages: int