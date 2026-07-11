from unittest.mock import patch

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.dependencies.authentication import get_current_user
from app.dependencies.database import get_db
from app.exceptions.sprint_exceptions import (
    DoneIssueCannotBeAddedException,
)
from main import app

client = TestClient(app)

ADMIN_ID = "507f1f77bcf86cd799439012"
PROJECT_ID = "507f1f77bcf86cd799439011"
SPRINT_ID = "507f1f77bcf86cd799439011"
ISSUE_ID = "507f1f77bcf86cd799439012"


def override_get_db():
    return {}


def override_get_current_user():
    return {
        "_id": ObjectId(ADMIN_ID),
        "name": "Admin",
        "email": "admin@gmail.com",
        "role": "admin",
    }


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    yield

    app.dependency_overrides.clear()


@patch("app.router.sprint.SprintService")
def test_create_sprint_success(mock_sprint_service):
    mock_sprint_service.return_value.create_sprint.return_value = "mock_sprint_id"

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

    assert response.status_code == 200
    assert response.json()["message"] == "Sprint created successfully."
    assert response.json()["sprint_id"] == "mock_sprint_id"


@patch("app.router.sprint.SprintService")
def test_add_issue_to_sprint_success(mock_sprint_service):
    mock_sprint_service.return_value.add_issue_to_sprint.return_value = None

    response = client.post(
        f"/sprints/{SPRINT_ID}/issues",
        json={
            "issue_id": ISSUE_ID,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Issue added to sprint successfully."


@patch("app.router.sprint.SprintService")
def test_prevent_adding_done_issue(mock_sprint_service):
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
    assert response.json()["detail"] == "DONE issues cannot be added to sprint"