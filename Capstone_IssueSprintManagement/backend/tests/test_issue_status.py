from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from app.exceptions.issue_exceptions import (
    AssigneeRequiredException,
    InvalidIssueStatusTransitionException,
)

client = TestClient(app)


@patch("app.router.issue.mongodb.db", new={})
@patch("app.router.issue.IssueService")
def test_valid_status_transition(mock_issue_service):
    response = client.patch(
        "/projects/issues/507f1f77bcf86cd799439011/status",
        json={
            "status": "in_progress",
            "updated_by": "507f1f77bcf86cd799439012",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Issue status updated successfully."


@patch("app.router.issue.mongodb.db", new={})
@patch("app.router.issue.IssueService")
def test_invalid_status_transition_done_to_todo(mock_issue_service):
    mock_issue_service.return_value.update_issue_status.side_effect = (
        InvalidIssueStatusTransitionException()
    )

    response = client.patch(
        "/projects/issues/507f1f77bcf86cd799439011/status",
        json={
            "status": "todo",
            "updated_by": "507f1f77bcf86cd799439012",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid issue status transition"


@patch("app.router.issue.mongodb.db", new={})
@patch("app.router.issue.IssueService")
def test_non_assignee_update_invalid(mock_issue_service):
    mock_issue_service.return_value.update_issue_status.side_effect = (
        AssigneeRequiredException()
    )

    response = client.patch(
        "/projects/issues/507f1f77bcf86cd799439011/status",
        json={
            "status": "in_progress",
            "updated_by": "507f1f77bcf86cd799439013",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Only the assigned user can update issue status"