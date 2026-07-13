from typing import List

from fastapi import APIRouter, Depends, Query
from app.dependencies.authentication import get_current_user
from app.dependencies.authorization import RoleChecker
from app.dependencies.database import get_db
from app.schemas.requests.issue_request import (
    CreateCommentRequest,
    CreateIssueRequest,
    UpdateCommentRequest,
    UpdateIssueStatusRequest,
)
from app.schemas.responses.issue_response import (
    CommentResponse,
    CreateIssueResponse,
    IssueListResponse,
    UpdateIssueStatusResponse,
    StoryOptionResponse,
)
from app.services.issue_service import IssueService

router = APIRouter()

admin_or_member_required = RoleChecker(["admin", "member"])

@router.post("/{project_id}/issues", response_model=CreateIssueResponse)
def create_issue(
    project_id: str,
    issue: CreateIssueRequest,
    _current_user: dict = Depends(admin_or_member_required),
    db=Depends(get_db)
    ):
    """
    Create a new issue inside a project.
    """

    issue_service = IssueService(db)
    issue_id = issue_service.create_issue(project_id, issue)

    return {
        "message": "Issue created successfully.",
        "issue_id": issue_id,
        }

@router.get("/{project_id}/issues", response_model=IssueListResponse)
def get_project_issues(
    project_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1, le=50),
    status: str | None = Query(None),
    priority: str | None = Query(None),
    assignee: str | None = Query(None),
    search: str | None = Query(None),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Fetch project issues with pagination and filter.
    """
    issue_service = IssueService(db)

    return issue_service.get_project_issues(
        project_id=project_id,
        page=page,
        limit=limit,
        status=status,
        priority=priority,
        assignee=assignee,
        search=search,
    )


@router.patch("/issues/{issue_id}/status", response_model=UpdateIssueStatusResponse)
def update_issue_status(
    issue_id: str,
    request: UpdateIssueStatusRequest,
    current_user: dict = Depends(admin_or_member_required),
    db=Depends(get_db)
):
    """
    Update issue status.
    """

    issue_service = IssueService(db)
    issue_service.update_issue_status(issue_id, request, current_user)

    return {"message": "Issue status updated successfully."}

@router.get("/{project_id}/stories",response_model=List[StoryOptionResponse],)
def get_project_stories(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """
    Fetch story issues for project.
    """

    issue_service = IssueService(db)

    return issue_service.get_project_stories(project_id)


@router.post("/issues/{issue_id}/comments", response_model=CommentResponse)
def add_comment(
    issue_id: str,
    request: CreateCommentRequest,
    current_user: dict = Depends(admin_or_member_required),
    db=Depends(get_db)
):
    """
    Add own comment.
    """

    issue_service = IssueService(db)
    issue_service.add_comment(issue_id, request)

    return {
        "message": "Comment added successfully."
    }

@router.put("/issues/{issue_id}/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    issue_id: str,
    comment_id: str,
    request: UpdateCommentRequest,
    current_user: dict = Depends(admin_or_member_required),
    db=Depends(get_db),
):
    """
    Update own comment.
    """

    issue_service = IssueService(db)
    issue_service.update_comment(issue_id, comment_id, request)

    return {
        "message": "Comment updated successfully."
    }

@router.delete("/issues/{issue_id}/comments/{comment_id}", response_model=CommentResponse)
def delete_comment(
    issue_id: str,
    comment_id: str,
    user_id: str,
    current_user: dict = Depends(admin_or_member_required),
    db=Depends(get_db),
):
    """
    Delete own comment.
    """

    issue_service = IssueService(db)
    issue_service.delete_comment(issue_id, comment_id, user_id)

    return {
        "message": "Comment deleted successfully."
    }