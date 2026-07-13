from fastapi import APIRouter, Depends, Query

from app.dependencies.database import get_db
from app.schemas.requests.sprint_request import (
    CreateSprintRequest,
    SprintIssueRequest,
    SprintStatusRequest,
)
from app.schemas.responses.sprint_response import (
    CreateSprintResponse,
    SprintListResponse,
    SprintStatusResponse,
)
from app.services.sprint_service import SprintService

router = APIRouter()


@router.post("/", response_model=CreateSprintResponse)
def create_sprint(request: CreateSprintRequest, db=Depends(get_db)):
    """
    Create a new sprint.
    """
    sprint_service = SprintService(db)
    sprint_id = sprint_service.create_sprint(request)

    return {
        "message": "Sprint created successfully.",
        "sprint_id": sprint_id,
    }


@router.post("/{sprint_id}/issues", response_model=SprintStatusResponse)
def add_issue_to_sprint(sprint_id: str, request: SprintIssueRequest, db=Depends(get_db)):
    """
    Add issues to sprint.
    """

    sprint_service = SprintService(db)
    sprint_service.add_issue_to_sprint(sprint_id, request.issue_id)

    return {"message": "Issue added to sprint successfully."}


@router.delete("/{sprint_id}/issues", response_model=SprintStatusResponse)
def remove_issue_from_sprint(sprint_id: str, request: SprintIssueRequest, db=Depends(get_db)):
    """
    Remove issue from the sprint.
    """
    sprint_service = SprintService(db)
    sprint_service.remove_issue_from_sprint(sprint_id, request.issue_id)

    return {"message": "Issue removed from sprint successfully."}


@router.get("/", response_model=SprintListResponse)
def get_sprints(
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1, le=50),
    project_id: str | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None),
    db=Depends(get_db),
):
    """
    Fetch sprints with pagination and filters.
    """

    sprint_service = SprintService(db)

    return sprint_service.get_sprints(
        page=page,
        limit=limit,
        project_id=project_id,
        status=status,
        search=search,
    )

@router.patch("/{sprint_id}/start", response_model=SprintStatusResponse)
def start_sprint(sprint_id: str, request: SprintStatusRequest, db=Depends(get_db)):
    """
    Start a sprint.
    """
    sprint_service = SprintService(db)
    sprint_service.start_sprint(sprint_id, request.updated_by)

    return {"message": "Sprint started successfully."}


@router.patch("/{sprint_id}/complete", response_model=SprintStatusResponse)
def complete_sprint(sprint_id: str, request: SprintStatusRequest, db=Depends(get_db)):
    """
    Complete an active sprint.
    """
    sprint_service = SprintService(db)
    sprint_service.complete_sprint(sprint_id, request.updated_by)

    return {"message": "Sprint completed successfully."}