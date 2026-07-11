from fastapi import APIRouter, HTTPException, Query

from app.database import mongodb
from pydantic import EmailStr

from typing import List
from app.schemas.project_schema import ProjectUpdate, ProjectListResponse

from app.schemas.project_schema import (
    ProjectCreate,
    ProjectResponse,
    ProjectMemberRequest,
    ProjectMemberResponse,
)
from app.services.project_service import ProjectService

router = APIRouter()


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, admin_email: EmailStr = Query(...)):

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )

    project_service = ProjectService(mongodb.db)
    project_id = project_service.create_project(project, admin_email)

    return {
            "message": "Project created successfully",
            "project_id": project_id
        }


@router.post("/{project_id}/members", response_model=ProjectMemberResponse)
def add_member(project_id: str, request: ProjectMemberRequest):

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )


    project_service = ProjectService(mongodb.db)
    project_service.add_member(
            project_id=project_id,
            admin_email=request.admin_email,
            member_email=request.member_email
        )

    return {"message": "Member added successfully"}



@router.delete("/{project_id}/members", response_model=ProjectMemberResponse)
def remove_member(project_id: str, request: ProjectMemberRequest):

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )


    project_service = ProjectService(mongodb.db)
    project_service.remove_member(
            project_id=project_id,
            admin_email=request.admin_email,
            member_email=request.member_email
        )

    return {"message": "Member removed successfully"}


@router.get("/", response_model=List[ProjectListResponse])
def get_projects():
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    project_service = ProjectService(mongodb.db)
    return project_service.get_all_projects()


@router.put("/{project_id}")
def update_project(project_id: str, project: ProjectUpdate):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database connection not initialized")

    project_service = ProjectService(mongodb.db)
    project_service.update_project(project_id, project)

    return {"message": "Project updated successfully"}