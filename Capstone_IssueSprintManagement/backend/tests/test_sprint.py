from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from app.exceptions.sprint_exceptions import DoneIssueCannotBeAddedException

client = TestClient(app)


@patch("app.router.sprint.mongodb.db", new={})
@patch("app.router.sprint.SprintService")
def test_create_sprint_success(mock_sprint_service):
    mock_sprint_service.return_value.create_sprint.return_value = "mock_sprint_id"

    response = client.post(
        "/sprints/",
        json={
            "name": "Sprint 1",
            "project_id": "507f1f77bcf86cd799439011",
            "created_by": "507f1f77bcf86cd799439012",
            "start_date": "2026-07-06",
            "end_date": "2026-07-15",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Sprint created successfully."
    assert response.json()["sprint_id"] == "mock_sprint_id"


@patch("app.router.sprint.mongodb.db", new={})
@patch("app.router.sprint.SprintService")
def test_add_issue_to_sprint_success(mock_sprint_service):
    response = client.post(
        "/sprints/507f1f77bcf86cd799439011/issues",
        json={
            "issue_id": "507f1f77bcf86cd799439012",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Issue added to sprint successfully."


@patch("app.router.sprint.mongodb.db", new={})
@patch("app.router.sprint.SprintService")
def test_prevent_adding_done_issue(mock_sprint_service):
    mock_sprint_service.return_value.add_issue_to_sprint.side_effect = (
        DoneIssueCannotBeAddedException()
    )

    response = client.post(
        "/sprints/507f1f77bcf86cd799439011/issues",
        json={
            "issue_id": "507f1f77bcf86cd799439012",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "DONE issues cannot be added to sprint"