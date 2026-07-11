from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app
from app.exceptions.user_exceptions import AdminAccessRequiredException
from app.exceptions.project_exceptions import (
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
)

client = TestClient(app)


@patch("app.router.project.mongodb.db", new={})
@patch("app.router.project.ProjectService")
def test_admin_can_create_project(mock_project_service):
    mock_project_service.return_value.create_project.return_value = (
        "mock_project_id"
    )

    response = client.post(
        "/projects/",
        params={"admin_email": "admin@example.com"},
        json={
            "name": "Sprint Management",
            "description": "Project for sprint planning",
            "project_key": "SPR1",
            "members": [],
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Project created successfully"
    assert response.json()["project_id"] == "mock_project_id"


@patch("app.router.project.mongodb.db", new={})
@patch("app.router.project.ProjectService")
def test_member_cannot_create_project(mock_project_service):
    mock_project_service.return_value.create_project.side_effect = (
        AdminAccessRequiredException()
    )

    response = client.post(
        "/projects/",
        params={"admin_email": "member@example.com"},
        json={
            "name": "Member Project",
            "description": "Member cannot create project",
            "project_key": "MEM1",
            "members": [],
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@patch("app.router.project.mongodb.db", new={})
@patch("app.router.project.ProjectService")
def test_admin_can_add_member_to_project(mock_project_service):
    mock_project_service.return_value.add_member.return_value = None

    response = client.post(
        "/projects/mock_project_id/members",
        json={
            "admin_email": "admin@example.com",
            "member_email": "member@example.com",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Member added successfully"


@patch("app.router.project.mongodb.db", new={})
@patch("app.router.project.ProjectService")
def test_add_duplicate_member_returns_conflict(mock_project_service):
    mock_project_service.return_value.add_member.side_effect = (
        MemberAlreadyAssignedException()
    )

    response = client.post(
        "/projects/mock_project_id/members",
        json={
            "admin_email": "admin@example.com",
            "member_email": "member@example.com",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Member already assigned to project"


@patch("app.router.project.mongodb.db", new={})
@patch("app.router.project.ProjectService")
def test_admin_can_remove_member_from_project(mock_project_service):
    mock_project_service.return_value.remove_member.return_value = None

    response = client.request(
        "DELETE",
        "/projects/mock_project_id/members",
        json={
            "admin_email": "admin@example.com",
            "member_email": "member@example.com",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Member removed successfully"


@patch("app.router.project.mongodb.db", new={})
@patch("app.router.project.ProjectService")
def test_remove_unassigned_member_returns_conflict(mock_project_service):
    mock_project_service.return_value.remove_member.side_effect = (
        MemberNotAssignedException()
    )

    response = client.request(
        "DELETE",
        "/projects/mock_project_id/members",
        json={
            "admin_email": "admin@example.com",
            "member_email": "member@example.com",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Member is not assigned to project"