from unittest.mock import patch

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.dependencies.authentication import get_current_user
from app.dependencies.database import get_db
from app.exceptions.project_exceptions import ProjectNotFoundException
from app.exceptions.sprint_exceptions import (
    DoneIssueCannotBeAddedException,
    InvalidSprintStatusException,
    SprintAlreadyExistsException,
    SprintNotFoundException,
)
from main import app


ADMIN_ID = "507f1f77bcf86cd799439012"
PROJECT_ID = "507f1f77bcf86cd799439011"
ISSUE_ID = "507f1f77bcf86cd799439012"
SPRINT_ID = "507f1f77bcf86cd799439011"

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


@pytest.fixture(autouse=True)
def override_dependencies():
    """
    Apply mock database and authenticated admin user
    before every test.
    """
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_admin_user

    yield

    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_current_user, None)


def test_create_sprint_invalid_date_range():
    response = client.post(
        "/sprints/",
        json={
            "name": "Sprint 1",
            "project_id": PROJECT_ID,
            "created_by": ADMIN_ID,
            "start_date": "2026-07-15",
            "end_date": "2026-07-10",
        },
    )

    assert response.status_code == 422


@patch("app.router.sprint.SprintService")
def test_duplicate_sprint_name(mock_sprint_service):
    mock_sprint_service.return_value.create_sprint.side_effect = (
        SprintAlreadyExistsException()
    )

    response = client.post(
        "/sprints/",
        json={
            "name": "Sprint 1",
            "project_id": PROJECT_ID,
            "created_by": ADMIN_ID,
            "start_date": "2026-07-10",
            "end_date": "2026-07-15",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Sprint name already exists in this project"
    )


@patch("app.router.sprint.SprintService")
def test_create_sprint_project_not_found(mock_sprint_service):
    mock_sprint_service.return_value.create_sprint.side_effect = (
        ProjectNotFoundException()
    )

    response = client.post(
        "/sprints/",
        json={
            "name": "Sprint 1",
            "project_id": PROJECT_ID,
            "created_by": ADMIN_ID,
            "start_date": "2026-07-10",
            "end_date": "2026-07-15",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


@patch("app.router.sprint.SprintService")
def test_add_done_issue_to_sprint(mock_sprint_service):
    mock_sprint_service.return_value.add_issue_to_sprint.side_effect = (
        DoneIssueCannotBeAddedException()
    )

    response = client.post(
        f"/sprints/{SPRINT_ID}/issues",
        json={
            "issue_id": ISSUE_ID,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "DONE issues cannot be added to sprint"
    )


@patch("app.router.sprint.SprintService")
def test_start_sprint_not_found(mock_sprint_service):
    mock_sprint_service.return_value.start_sprint.side_effect = (
        SprintNotFoundException()
    )

    response = client.patch(
        f"/sprints/{SPRINT_ID}/start",
        json={
            "updated_by": ADMIN_ID,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sprint not found"


@patch("app.router.sprint.SprintService")
def test_complete_non_active_sprint(mock_sprint_service):
    mock_sprint_service.return_value.complete_sprint.side_effect = (
        InvalidSprintStatusException()
    )

    response = client.patch(
        f"/sprints/{SPRINT_ID}/complete",
        json={
            "updated_by": ADMIN_ID,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Invalid sprint status transition"
    )