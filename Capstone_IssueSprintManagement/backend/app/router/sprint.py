from fastapi import APIRouter, HTTPException, Query

from app.database import mongodb
from app.exceptions.project_exceptions import ProjectNotFoundException
from app.exceptions.sprint_exceptions import (
    DoneIssueCannotBeAddedException,
    IssueAlreadyInSprintException,
    SprintCreationFailedException,
    SprintNotFoundException,
    SprintAlreadyExistsException,
)
from app.exceptions.user_exceptions import UserNotFoundException
from app.schemas.requests.sprint_request import (
    CreateSprintRequest,
    SprintIssueRequest,
)
from app.schemas.responses.sprint_response import (
    CreateSprintResponse,
    SprintIssueResponse,
    SprintListResponse,
)
from app.services.sprint_service import SprintService

router = APIRouter()


@router.post("/", response_model=CreateSprintResponse)
def create_sprint(request: CreateSprintRequest):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database connection not initialized.")

    try:
        sprint_service = SprintService(mongodb.db)
        sprint_id = sprint_service.create_sprint(request)

        return {
            "message": "Sprint created successfully.",
            "sprint_id": sprint_id,
        }

    except ProjectNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)

    except UserNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)

    except SprintCreationFailedException as exc:
        raise HTTPException(status_code=400, detail=exc.message)

    except SprintAlreadyExistsException as exc:
        raise HTTPException(status_code=409, detail=exc.message,)


@router.post("/{sprint_id}/issues", response_model=SprintIssueResponse)
def add_issue_to_sprint(sprint_id: str, request: SprintIssueRequest):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database connection not initialized.")

    try:
        sprint_service = SprintService(mongodb.db)
        sprint_service.add_issue_to_sprint(sprint_id, request.issue_id)

        return {"message": "Issue added to sprint successfully."}

    except SprintNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)

    except DoneIssueCannotBeAddedException as exc:
        raise HTTPException(status_code=400, detail=exc.message)

    except IssueAlreadyInSprintException as exc:
        raise HTTPException(status_code=409, detail=exc.message)


@router.delete("/{sprint_id}/issues", response_model=SprintIssueResponse)
def remove_issue_from_sprint(sprint_id: str, request: SprintIssueRequest):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database connection not initialized.")

    try:
        sprint_service = SprintService(mongodb.db)
        sprint_service.remove_issue_from_sprint(sprint_id, request.issue_id)

        return {"message": "Issue removed from sprint successfully."}

    except SprintNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.get("/", response_model=SprintListResponse)
def get_sprints(
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1, le=50),
    project_id: str | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None),
):
    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized.",
        )

    sprint_service = SprintService(mongodb.db)

    return sprint_service.get_sprints(
        page=page,
        limit=limit,
        project_id=project_id,
        status=status,
        search=search,
    )