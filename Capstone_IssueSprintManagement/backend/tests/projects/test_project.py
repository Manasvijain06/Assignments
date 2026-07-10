from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import get_db
from app.exceptions.project_exceptions import (
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
)
from app.exceptions.user_exceptions import AdminAccessRequiredException
from main import app

client = TestClient(app)


def override_get_db():
    return {}


app.dependency_overrides[get_db] = override_get_db


@patch("app.router.project.ProjectService")
def test_admin_can_create_project(mock_project_service):
    mock_project_service.return_value.create_project.return_value = "mock_project_id"

    response = client.post(
        "/projects/",
        params={"admin_id": "507f1f77bcf86cd799439012"},
        json={
            "name": "Sprint Management",
            "description": "Project for sprint planning",
            "project_key": "SPR1",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Project created successfully."
    assert response.json()["project_id"] == "mock_project_id"


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
def test_admin_can_add_member_to_project(mock_project_service):
    mock_project_service.return_value.add_member.return_value = None

    response = client.post(
        "/projects/mock_project_id/members",
        json={
            "admin_id": "507f1f77bcf86cd799439012",
            "member_id": "507f1f77bcf86cd799439013",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Member added successfully."


@patch("app.router.project.ProjectService")
def test_add_duplicate_member_returns_conflict(mock_project_service):
    mock_project_service.return_value.add_member.side_effect = (
        MemberAlreadyAssignedException()
    )

    response = client.post(
        "/projects/mock_project_id/members",
        json={
            "admin_id": "507f1f77bcf86cd799439012",
            "member_id": "507f1f77bcf86cd799439013",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Member already assigned to project"


@patch("app.router.project.ProjectService")
def test_admin_can_remove_member_from_project(mock_project_service):
    mock_project_service.return_value.remove_member.return_value = None

    response = client.request(
        "DELETE",
        "/projects/mock_project_id/members",
        json={
            "admin_id": "507f1f77bcf86cd799439012",
            "member_id": "507f1f77bcf86cd799439013",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Member removed successfully."


@patch("app.router.project.ProjectService")
def test_remove_unassigned_member_returns_conflict(mock_project_service):
    mock_project_service.return_value.remove_member.side_effect = (
        MemberNotAssignedException()
    )

    response = client.request(
        "DELETE",
        "/projects/mock_project_id/members",
        json={
            "admin_id": "507f1f77bcf86cd799439012",
            "member_id": "507f1f77bcf86cd799439013",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Member is not assigned to project"