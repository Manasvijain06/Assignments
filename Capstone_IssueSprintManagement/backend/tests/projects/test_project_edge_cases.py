from unittest.mock import patch

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.dependencies.authentication import get_current_user
from app.dependencies.database import get_db
from app.exceptions.project_exceptions import (
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
)
from main import app


ADMIN_ID = "507f1f77bcf86cd799439012"
MEMBER_ID = "507f1f77bcf86cd799439013"
PROJECT_ID = "507f1f77bcf86cd799439011"

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
def test_duplicate_project_key(mock_project_service):
    mock_project_service.return_value.create_project.side_effect = (
        ProjectAlreadyExistsException()
    )

    response = client.post(
        "/projects/",
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
def test_update_project_not_found(mock_project_service):
    mock_project_service.return_value.update_project.side_effect = (
        ProjectNotFoundException()
    )

    response = client.put(
        f"/projects/{PROJECT_ID}",
        json={
            "description": "Updated description",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_create_project_missing_fields():
    response = client.post(
        "/projects/",
        json={
            "name": "Only Name",
        },
    )

    assert response.status_code == 422