from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import get_db
from app.exceptions.project_exceptions import (
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
)
from app.exceptions.user_exceptions import AdminAccessRequiredException
from main import app

client = TestClient(app)


def override_get_db():
    return {}


app.dependency_overrides[get_db] = override_get_db


@patch("app.router.project.ProjectService")
def test_duplicate_project_key(mock_project_service):
    mock_project_service.return_value.create_project.side_effect = (
        ProjectAlreadyExistsException()
    )

    response = client.post(
        "/projects/",
        params={"admin_id": "507f1f77bcf86cd799439012"},
        json={
            "name": "Sprint Management",
            "description": "Project for sprint planning",
            "project_key": "SPR1",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Project key already exists"


@patch("app.router.project.ProjectService")
def test_member_cannot_create_project(mock_project_service):
    mock_project_service.return_value.create_project.side_effect = (
        AdminAccessRequiredException()
    )

    response = client.post(
        "/projects/",
        params={"admin_id": "507f1f77bcf86cd799439013"},
        json={
            "name": "Member Project",
            "description": "Member cannot create project",
            "project_key": "MEM1",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@patch("app.router.project.ProjectService")
def test_update_project_not_found(mock_project_service):
    mock_project_service.return_value.update_project.side_effect = (
        ProjectNotFoundException()
    )

    response = client.put(
        "/projects/507f1f77bcf86cd799439011",
        json={"description": "Updated description"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_create_project_missing_fields():
    response = client.post(
        "/projects/",
        params={"admin_id": "507f1f77bcf86cd799439012"},
        json={"name": "Only Name"},
    )

    assert response.status_code == 422