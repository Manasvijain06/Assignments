from fastapi import APIRouter, HTTPException

from app.database import mongodb
from app.exceptions.project_exceptions import ProjectNotFoundException
from app.exceptions.user_exceptions import UserNotFoundException
from app.schemas.requests.issue_request import CreateIssueRequest
from app.schemas.responses.issue_response import CreateIssueResponse
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