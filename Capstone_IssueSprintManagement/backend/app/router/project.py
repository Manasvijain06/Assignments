from typing import List

from fastapi import APIRouter, Depends, Query

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
    ProjectDetailResponse,
    ProjectMemberResponse,
    UpdateProjectResponse,
)
from app.services.project_service import ProjectService

router = APIRouter()


@router.post("/", response_model=CreateProjectResponse)
def create_project(project: CreateProjectRequest, admin_id: str = Query(...), db=Depends(get_db)):
    """
    Create a new project.
    """

    project_service = ProjectService(db)
    project_id = project_service.create_project(project, admin_id)

    return {
        "message": "Project created successfully.",
        "project_id": project_id,
    }


@router.get("/", response_model=List[ProjectDetailResponse])
def get_all_projects(db=Depends(get_db)):
    """
    Fetch all projects.
    """

    project_service = ProjectService(db)

    return project_service.get_all_projects()


@router.put("/{project_id}", response_model=UpdateProjectResponse)
def update_project(project_id: str, project: UpdateProjectRequest, db=Depends(get_db)):
    """
    Update project description.
    """
    project_service = ProjectService(db)

    project_service.update_project(project_id, project)

    return {
        "message": "Project updated successfully."
    }


@router.delete("/{project_id}", response_model=DeleteProjectResponse)
def delete_project(project_id: str, db=Depends(get_db)):
    """
    Delete a project.
    """

    project_service = ProjectService(db)
    project_service.delete_project(project_id)

    return {
        "message": "Project deleted successfully."
    }

@router.post("/{project_id}/members", response_model=ProjectMemberResponse)
def add_member(project_id: str, request: AddMemberRequest, db=Depends(get_db)):
    """
    Add a member to a project.
    """

    project_service = ProjectService(db)

    project_service.add_member(
        project_id,
        request.admin_id,
        request.member_id,
    )

    return {
        "message": "Member added successfully."
    }


@router.delete("/{project_id}/members", response_model=ProjectMemberResponse)
def remove_member(project_id: str, request: RemoveMemberRequest, db=Depends(get_db)):
    """
    Remove a member from a project.
    """
    project_service = ProjectService(db)

    project_service.remove_member(
        project_id,
        request.admin_id,
        request.member_id,
    )

    return {
        "message": "Member removed successfully."
    }
