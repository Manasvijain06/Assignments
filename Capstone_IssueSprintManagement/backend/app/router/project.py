from fastapi import APIRouter, HTTPException, Query

from app.database import mongodb

from typing import List
from app.exceptions.project_exceptions import (
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
)
from app.exceptions.user_exceptions import (
    AdminAccessRequiredException,
    UserNotFoundException,
)
from app.schemas.requests.project_request import (
    AddMemberRequest,
    RemoveMemberRequest,
    UpdateProjectRequest,
    CreateProjectRequest,
)
from app.schemas.responses.project_response import (
    CreateProjectResponse,
    DeleteProjectResponse,
    ProjectDetailResponse,
    ProjectMemberResponse,
    UpdateProjectResponse,
)
from app.services.project_service import ProjectService

router = APIRouter()


@router.post("/", response_model=CreateProjectResponse)
def create_project(project: CreateProjectRequest, admin_id: str = Query(...)):

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )

    try:
        project_service = ProjectService(mongodb.db)

        project_id = project_service.create_project(
            project,
            admin_id,
        )

        return {
            "message": "Project created successfully.",
            "project_id": project_id,
        }

    except ProjectAlreadyExistsException as exc:
        raise HTTPException(409, exc.message)

    except UserNotFoundException as exc:
        raise HTTPException(404, exc.message)

    except AdminAccessRequiredException as exc:
        raise HTTPException(403, exc.message)


@router.get("/", response_model=List[ProjectDetailResponse])
def get_all_projects():
    """
    Fetch all projects.
    """
    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized",
        )

    project_service = ProjectService(mongodb.db)
    return project_service.get_all_projects()


@router.put("/{project_id}", response_model=UpdateProjectResponse,)
def update_project(project_id: str, project: UpdateProjectRequest):
    """
    Update project description.
    """
    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )

    try:
        project_service = ProjectService(mongodb.db)

        project_service.update_project(
            project_id,
            project,
        )

        return {
            "message": "Project updated successfully."
        }

    except ProjectNotFoundException as exc:
        raise HTTPException(404, exc.message)


@router.delete("/{project_id}", response_model=DeleteProjectResponse)
def delete_project(project_id: str):
    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )

    try:
        project_service = ProjectService(mongodb.db)

        project_service.delete_project(project_id)

        return {
            "message": "Project deleted successfully."
        }

    except ProjectNotFoundException as exc:
        raise HTTPException(404, exc.message)

@router.post("/{project_id}/members", response_model=ProjectMemberResponse)
def add_member(project_id: str, request: AddMemberRequest):
    """
    Add a member to a project.
    """

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )


    try:
        project_service = ProjectService(mongodb.db)

        project_service.add_member(
            project_id,
            request.admin_id,
            request.member_id,
        )

        return {
            "message": "Member added successfully."
        }

    except (
        ProjectNotFoundException,
        UserNotFoundException,
    ) as exc:
        raise HTTPException(404, exc.message)

    except MemberAlreadyAssignedException as exc:
        raise HTTPException(409, exc.message)

    except AdminAccessRequiredException as exc:
        raise HTTPException(403, exc.message)

@router.delete("/{project_id}/members", response_model=ProjectMemberResponse)
def remove_member(project_id: str, request: RemoveMemberRequest):

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )


    try:
        project_service = ProjectService(mongodb.db)

        project_service.remove_member(
            project_id,
            request.admin_id,
            request.member_id,
        )

        return {
            "message": "Member removed successfully."
        }

    except (
        ProjectNotFoundException,
        UserNotFoundException,
    ) as exc:
        raise HTTPException(404, exc.message)

    except MemberNotAssignedException as exc:
        raise HTTPException(409, exc.message)

    except AdminAccessRequiredException as exc:
        raise HTTPException(403, exc.message)
