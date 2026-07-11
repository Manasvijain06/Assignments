from unittest.mock import patch

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.dependencies.authentication import get_current_user
from app.dependencies.database import get_db
from app.exceptions.project_exceptions import (
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
)
from main import app


ADMIN_ID = "507f1f77bcf86cd799439012"
MEMBER_ID = "507f1f77bcf86cd799439013"

client = TestClient(app)


def override_get_db():
    return {}


def override_admin_user():
    return {
        "_id": ObjectId(ADMIN_ID),
        "name": "Admin User",
        "email": "admin@gmail.com",
        "role": "admin",
    }


def override_member_user():
    return {
        "_id": ObjectId(MEMBER_ID),
        "name": "Member User",
        "email": "member@gmail.com",
        "role": "member",
    }


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_admin_user

    yield

    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_current_user, None)


@patch("app.router.project.ProjectService")
def test_admin_can_create_project(mock_project_service):
    mock_project_service.return_value.create_project.return_value = (
        "mock_project_id"
    )

    response = client.post(
        "/projects/",
        json={
            "name": "Sprint Management",
            "description": "Project for sprint planning",
            "project_key": "SPR1",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Project created successfully."
    assert response.json()["project_id"] == "mock_project_id"

    mock_project_service.return_value.create_project.assert_called_once()

    project_request, admin_id = (
        mock_project_service.return_value.create_project.call_args.args
    )

    assert project_request.name == "Sprint Management"
    assert project_request.project_key == "SPR1"
    assert admin_id == ADMIN_ID


@patch("app.router.project.ProjectService")
def test_member_cannot_create_project(mock_project_service):
    app.dependency_overrides[get_current_user] = override_member_user

    response = client.post(
        "/projects/",
        json={
            "name": "Member Project",
            "description": "Member cannot create project",
            "project_key": "MEM1",
        },
    )

    assert response.status_code == 403

    assert response.json()["detail"] in {
        "Admin access required",
        "Admin access required.",
        "You are not allowed to perform this action.",
        "You are not authorized to perform this action.",
    }

    mock_project_service.return_value.create_project.assert_not_called()


@patch("app.router.project.ProjectService")
def test_admin_can_add_member_to_project(mock_project_service):
    mock_project_service.return_value.add_member.return_value = None

    response = client.post(
        "/projects/mock_project_id/members",
        json={
            "member_id": MEMBER_ID,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Member added successfully."

    mock_project_service.return_value.add_member.assert_called_once_with(
        "mock_project_id",
        ADMIN_ID,
        MEMBER_ID,
    )


@patch("app.router.project.ProjectService")
def test_add_duplicate_member_returns_conflict(mock_project_service):
    mock_project_service.return_value.add_member.side_effect = (
        MemberAlreadyAssignedException()
    )

    response = client.post(
        "/projects/mock_project_id/members",
        json={
            "member_id": MEMBER_ID,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Member already assigned to project"
    )


@patch("app.router.project.ProjectService")
def test_admin_can_remove_member_from_project(mock_project_service):
    mock_project_service.return_value.remove_member.return_value = None

    response = client.request(
        "DELETE",
        "/projects/mock_project_id/members",
        json={
            "member_id": MEMBER_ID,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Member removed successfully."

    mock_project_service.return_value.remove_member.assert_called_once_with(
        "mock_project_id",
        ADMIN_ID,
        MEMBER_ID,
    )


@patch("app.router.project.ProjectService")
def test_remove_unassigned_member_returns_conflict(mock_project_service):
    mock_project_service.return_value.remove_member.side_effect = (
        MemberNotAssignedException()
    )

    response = client.request(
        "DELETE",
        "/projects/mock_project_id/members",
        json={
            "member_id": MEMBER_ID,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Member is not assigned to project"
    )