from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import get_db
from app.exceptions.project_exceptions import ProjectNotFoundException
from app.exceptions.sprint_exceptions import (
    DoneIssueCannotBeAddedException,
    InvalidSprintStatusException,
    SprintAlreadyExistsException,
    SprintNotFoundException,
)
from main import app

client = TestClient(app)


def override_get_db():
    return {}


app.dependency_overrides[get_db] = override_get_db


def test_create_sprint_invalid_date_range():
    response = client.post(
        "/sprints/",
        json={
            "name": "Sprint 1",
            "project_id": "507f1f77bcf86cd799439011",
            "created_by": "507f1f77bcf86cd799439012",
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
            "project_id": "507f1f77bcf86cd799439011",
            "created_by": "507f1f77bcf86cd799439012",
            "start_date": "2026-07-10",
            "end_date": "2026-07-15",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Sprint name already exists in this project"


@patch("app.router.sprint.SprintService")
def test_create_sprint_project_not_found(mock_sprint_service):
    mock_sprint_service.return_value.create_sprint.side_effect = (
        ProjectNotFoundException()
    )

    response = client.post(
        "/sprints/",
        json={
            "name": "Sprint 1",
            "project_id": "507f1f77bcf86cd799439011",
            "created_by": "507f1f77bcf86cd799439012",
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
        "/sprints/507f1f77bcf86cd799439011/issues",
        json={"issue_id": "507f1f77bcf86cd799439012"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "DONE issues cannot be added to sprint"


@patch("app.router.sprint.SprintService")
def test_start_sprint_not_found(mock_sprint_service):
    mock_sprint_service.return_value.start_sprint.side_effect = (
        SprintNotFoundException()
    )

    response = client.patch(
        "/sprints/507f1f77bcf86cd799439011/start",
        json={"updated_by": "507f1f77bcf86cd799439012"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sprint not found"


@patch("app.router.sprint.SprintService")
def test_complete_non_active_sprint(mock_sprint_service):
    mock_sprint_service.return_value.complete_sprint.side_effect = (
        InvalidSprintStatusException()
    )

    response = client.patch(
        "/sprints/507f1f77bcf86cd799439011/complete",
        json={"updated_by": "507f1f77bcf86cd799439012"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid sprint status transition"