from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.schemas.responses.auth_response import UserResponse


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


class ParentStoryResponse(BaseModel):
    issue_id: str
    issue_key: str
    title: str


class IssueCommentResponse(BaseModel):
    comment_id: str
    user: UserResponse
    comment: str
    created_at: datetime
    updated_at: datetime

class IssueDetailResponse(BaseModel):
    issue_id: str
    issue_key: str
    title: str
    description: str
    priority: str
    status: str
    type: str
    assignee: Optional[UserResponse]
    created_by: Optional[UserResponse]
    parent_story: Optional[ParentStoryResponse] = None
    comments: List[IssueCommentResponse] = []
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

class CommentResponse(BaseModel):
    message: str

