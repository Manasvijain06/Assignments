from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import get_db
from app.exceptions.issue_exceptions import (
    CommentNotFoundException,
    CommentPermissionDeniedException,
)
from main import app

client = TestClient(app)


def override_get_db():
    return {}


app.dependency_overrides[get_db] = override_get_db


@patch("app.router.issue.IssueService")
def test_add_comment_success(mock_issue_service):
    mock_issue_service.return_value.add_comment.return_value = None

    response = client.post(
        "/projects/issues/507f1f77bcf86cd799439011/comments",
        json={
            "user_id": "507f1f77bcf86cd799439012",
            "comment": "This issue needs to be fixed.",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Comment added successfully."


@patch("app.router.issue.IssueService")
def test_edit_comment_success(mock_issue_service):
    mock_issue_service.return_value.update_comment.return_value = None

    response = client.put(
        "/projects/issues/507f1f77bcf86cd799439011/comments/comment-1",
        json={
            "user_id": "507f1f77bcf86cd799439012",
            "comment": "Updated comment text.",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Comment updated successfully."


@patch("app.router.issue.IssueService")
def test_delete_comment_success(mock_issue_service):
    mock_issue_service.return_value.delete_comment.return_value = None

    response = client.delete(
        "/projects/issues/507f1f77bcf86cd799439011/comments/comment-1",
        params={"user_id": "507f1f77bcf86cd799439012"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Comment deleted successfully."


@patch("app.router.issue.IssueService")
def test_edit_comment_not_found(mock_issue_service):
    mock_issue_service.return_value.update_comment.side_effect = (
        CommentNotFoundException()
    )

    response = client.put(
        "/projects/issues/507f1f77bcf86cd799439011/comments/comment-1",
        json={
            "user_id": "507f1f77bcf86cd799439012",
            "comment": "Updated comment text.",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Comment not found"


@patch("app.router.issue.IssueService")
def test_delete_comment_permission_denied(mock_issue_service):
    mock_issue_service.return_value.delete_comment.side_effect = (
        CommentPermissionDeniedException()
    )

    response = client.delete(
        "/projects/issues/507f1f77bcf86cd799439011/comments/comment-1",
        params={"user_id": "507f1f77bcf86cd799439013"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You can update or delete only your own comments"
    )


@patch("app.router.issue.IssueService")
def test_search_results_accuracy(mock_issue_service):
    mock_issue_service.return_value.get_project_issues.return_value = {
        "items": [
            {
                "issue_id": "507f1f77bcf86cd799439011",
                "issue_key": "SPR1-1",
                "title": "Login bug",
                "description": "Login button is not working",
                "priority": "high",
                "status": "backlog",
                "type": "bug",
                "assignee": None,
                "created_by": None,
                "parent_story": None,
                "comments": [],
                "children": [],
            }
        ],
        "total": 1,
        "page": 1,
        "limit": 6,
        "total_pages": 1,
    }

    response = client.get(
        "/projects/507f1f77bcf86cd799439010/issues",
        params={
            "search": "Login",
            "page": 1,
            "limit": 6,
        },
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["title"] == "Login bug"
    assert response.json()["items"][0]["issue_key"] == "SPR1-1"