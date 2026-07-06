from typing import List, Optional
from pydantic import BaseModel, EmailStr


class CreateIssueResponse(BaseModel):
    """
    Response returned after creating an issue.
    """

    message: str
    issue_id: str

class UpdateIssueStatusResponse(BaseModel):
    """
    Response returned after updating an issue."""
    message: str

class IssueUserResponse(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    role: str

class ParentStoryResponse(BaseModel):
    issue_id: str
    issue_key: str
    title: str

class IssueDetailResponse(BaseModel):
    issue_id: str
    issue_key: str
    title: str
    description: str
    priority: str
    status: str
    type: str
    assignee: Optional[IssueUserResponse]
    created_by: Optional[IssueUserResponse]
    parent_story: Optional[ParentStoryResponse] = None
    children: List["IssueDetailResponse"] = []


class IssueListResponse(BaseModel):
    items: List[IssueDetailResponse]
    total: int
    page: int
    limit: int
    total_pages: int

class StoryOptionResponse(BaseModel):
    issue_id: str
    issue_key: str
    title: str