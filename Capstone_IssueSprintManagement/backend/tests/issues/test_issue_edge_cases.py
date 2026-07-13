from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import get_db
from app.exceptions.issue_exceptions import (
    AssigneeRequiredException,
    CommentPermissionDeniedException,
    InvalidIssueStatusTransitionException,
    IssueNotFoundException,
)
from app.exceptions.project_exceptions import ProjectNotFoundException
from main import app

client = TestClient(app)


def override_get_db():
    return {}


app.dependency_overrides[get_db] = override_get_db


@patch("app.router.issue.IssueService")
def test_create_issue_project_not_found(mock_issue_service):
    mock_issue_service.return_value.create_issue.side_effect = (
        ProjectNotFoundException()
    )

    response = client.post(
        "/projects/507f1f77bcf86cd799439011/issues",
        json={
            "title": "Login bug",
            "description": "Login button not working",
            "type": "bug",
            "priority": "high",
            "assignee": "507f1f77bcf86cd799439013",
            "created_by": "507f1f77bcf86cd799439012",
            "parent_id": None,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_create_issue_invalid_status_value():
    response = client.patch(
        "/projects/issues/507f1f77bcf86cd799439011/status",
        json={
            "status": "closed",
            "updated_by": "507f1f77bcf86cd799439012",
        },
    )

    assert response.status_code == 422


@patch("app.router.issue.IssueService")
def test_invalid_issue_status_transition(mock_issue_service):
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

    assert response.status_code == 409
    assert response.json()["detail"] == "Invalid issue status transition"


@patch("app.router.issue.IssueService")
def test_non_assignee_cannot_update_status(mock_issue_service):
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
    assert response.json()["detail"] == (
        "Only the assigned user can update issue status"
    )


@patch("app.router.issue.IssueService")
def test_issue_not_found(mock_issue_service):
    mock_issue_service.return_value.update_issue_status.side_effect = (
        IssueNotFoundException()
    )

    response = client.patch(
        "/projects/issues/507f1f77bcf86cd799439011/status",
        json={
            "status": "in_progress",
            "updated_by": "507f1f77bcf86cd799439012",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Issue not found"


@patch("app.router.issue.IssueService")
def test_user_cannot_edit_other_user_comment(mock_issue_service):
    mock_issue_service.return_value.update_comment.side_effect = (
        CommentPermissionDeniedException()
    )

    response = client.put(
        "/projects/issues/507f1f77bcf86cd799439011/comments/comment-1",
        json={
            "user_id": "507f1f77bcf86cd799439013",
            "comment": "Updated comment",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You can update or delete only your own comments"
    )