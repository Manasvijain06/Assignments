from fastapi import APIRouter, Depends, Query

from app.dependencies.authentication import get_current_user
from app.dependencies.authorization import RoleChecker
from app.dependencies.database import get_db

from app.schemas.requests.project_request import (
    AddMemberRequest,
    CreateProjectRequest,
    RemoveMemberRequest,
    UpdateProjectRequest,
)
from app.schemas.responses.project_response import (
    CreateProjectResponse,
    DeleteProjectResponse,
    ProjectListResponse,
    ProjectMemberResponse,
    UpdateProjectResponse,
)
from app.services.project_service import ProjectService

router = APIRouter()

admin_required = RoleChecker(["admin"])

@router.post("/", response_model=CreateProjectResponse)
def create_project(
    project: CreateProjectRequest,
    current_user: dict = Depends(admin_required),
    db=Depends(get_db)):
    """
    Create a new project.
    """

    project_service = ProjectService(db)
    admin_id = str(current_user["_id"])
    project_id = project_service.create_project(project, admin_id)

    return {
        "message": "Project created successfully.",
        "project_id": project_id,
    }


@router.get("/", response_model=ProjectListResponse)
def get_all_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1, le=50),
    current_user = Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Fetch all projects.
    """

    project_service = ProjectService(db)

    return project_service.get_all_projects(
        page=page,
        limit=limit,
    )


@router.put("/{project_id}", response_model=UpdateProjectResponse)
def update_project(project_id: str, project: UpdateProjectRequest,current_user = Depends(admin_required), db=Depends(get_db)):
    """
    Update project description.
    """
    project_service = ProjectService(db)

    project_service.update_project(project_id, project)

    return {
        "message": "Project updated successfully."
    }


@router.delete("/{project_id}", response_model=DeleteProjectResponse)
def delete_project(project_id: str, current_user = Depends(admin_required), db=Depends(get_db)):
    """
    Delete a project.
    """

    project_service = ProjectService(db)
    project_service.delete_project(project_id)

    return {
        "message": "Project deleted successfully."
    }

@router.post("/{project_id}/members", response_model=ProjectMemberResponse)
def add_member(project_id: str, request: AddMemberRequest, current_user = Depends(admin_required), db=Depends(get_db)):
    """
    Add a member to a project.
    """

    project_service = ProjectService(db)
    admin_id = str(current_user["_id"])

    project_service.add_member(
        project_id,
        admin_id,
        request.member_id,
    )

    return {
        "message": "Member added successfully."
    }


@router.delete("/{project_id}/members", response_model=ProjectMemberResponse)
def remove_member(project_id: str, request: RemoveMemberRequest,current_user = Depends(admin_required), db=Depends(get_db)):
    """
    Remove a member from a project.
    """
    project_service = ProjectService(db)
    admin_id = str(current_user["_id"])

    project_service.remove_member(
        project_id,
        admin_id,
        request.member_id,
    )

    return {
        "message": "Member removed successfully."
    }
