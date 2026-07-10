from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import get_db
from app.exceptions.project_exceptions import ProjectNotFoundException
from main import app

client = TestClient(app)


def override_get_db():
    return {}


app.dependency_overrides[get_db] = override_get_db


@patch("app.router.issue.IssueService")
def test_issue_creation_success(mock_issue_service):
    mock_issue_service.return_value.create_issue.return_value = "mock_issue_id"

    response = client.post(
        "/projects/507f1f77bcf86cd799439011/issues",
        json={
            "title": "Login bug",
            "description": "Login button is not working",
            "type": "bug",
            "priority": "high",
            "assignee": "507f1f77bcf86cd799439013",
            "created_by": "507f1f77bcf86cd799439012",
            "parent_id": None,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Issue created successfully."
    assert response.json()["issue_id"] == "mock_issue_id"


@patch("app.router.issue.IssueService")
def test_create_issue_invalid_project_id(mock_issue_service):
    mock_issue_service.return_value.create_issue.side_effect = (
        ProjectNotFoundException()
    )

    response = client.post(
        "/projects/invalid_project_id/issues",
        json={
            "title": "Login bug",
            "description": "Login button is not working",
            "type": "bug",
            "priority": "high",
            "assignee": "507f1f77bcf86cd799439013",
            "created_by": "507f1f77bcf86cd799439012",
            "parent_id": None,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_create_issue_missing_fields():
    response = client.post(
        "/projects/507f1f77bcf86cd799439011/issues",
        json={
            "title": "Login bug",
        },
    )

    assert response.status_code == 422