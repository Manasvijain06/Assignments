from typing import List
from fastapi import APIRouter, HTTPException, Query

from app.database import mongodb
from app.exceptions.issue_exceptions import (
    AssigneeRequiredException,
    InvalidIssueStatusTransitionException,
    IssueNotFoundException,
    InvalidParentIssueException,
)
from app.exceptions.project_exceptions import ProjectNotFoundException
from app.exceptions.user_exceptions import UserNotFoundException
from app.schemas.requests.issue_request import (
    CreateIssueRequest,
    UpdateIssueStatusRequest,
)
from app.schemas.responses.issue_response import (
    CreateIssueResponse,
    IssueListResponse,
    UpdateIssueStatusResponse,
    StoryOptionResponse,
)
from app.services.issue_service import IssueService

router = APIRouter()


@router.post(
    "/{project_id}/issues",
    response_model=CreateIssueResponse,
)
def create_issue(project_id: str, issue: CreateIssueRequest):
    """
    Create a new issue inside a project.
    """

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized.",
        )

    try:
        issue_service = IssueService(mongodb.db)
        issue_id = issue_service.create_issue(project_id, issue)

        return {
            "message": "Issue created successfully.",
            "issue_id": issue_id,
        }

    except ProjectNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)

    except UserNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)

    except InvalidParentIssueException as exc:
        raise HTTPException(status_code=400, detail=exc.message)

@router.get("/{project_id}/issues", response_model=IssueListResponse)
def get_project_issues(
    project_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1, le=50),
    status: str | None = Query(None),
    priority: str | None = Query(None),
    assignee: str | None = Query(None),
    search: str | None = Query(None),
):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database connection not initialized.")

    try:
        issue_service = IssueService(mongodb.db)

        return issue_service.get_project_issues(
            project_id=project_id,
            page=page,
            limit=limit,
            status=status,
            priority=priority,
            assignee=assignee,
            search=search,
        )

    except ProjectNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.patch("/issues/{issue_id}/status", response_model=UpdateIssueStatusResponse)
def update_issue_status(issue_id: str, request: UpdateIssueStatusRequest):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database connection not initialized.")

    try:
        issue_service = IssueService(mongodb.db)
        issue_service.update_issue_status(issue_id, request)

        return {"message": "Issue status updated successfully."}

    except IssueNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)

    except AssigneeRequiredException as exc:
        raise HTTPException(status_code=403, detail=exc.message)

    except InvalidIssueStatusTransitionException as exc:
        raise HTTPException(status_code=400, detail=exc.message)


@router.get("/{project_id}/stories",response_model=List[StoryOptionResponse],)
def get_project_stories(project_id: str):
    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized.",
        )

    try:
        issue_service = IssueService(mongodb.db)
        return issue_service.get_project_stories(project_id)

    except ProjectNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)