from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app
from app.exceptions.user_exceptions import (
    UserNotFoundException,
    AdminAccessRequiredException,
)

client = TestClient(app)


@patch("app.router.admin.mongodb.db", new={})
@patch("app.router.admin.UserService")
def test_admin_can_access_admin_endpoint(mock_user_service):
    mock_user_service.return_value.check_admin_access.return_value = {
        "email": "admin@example.com",
        "role": "admin",
    }

    response = client.get(
        "/users/admin-only",
        params={"email": "admin@example.com"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Admin access granted"
    assert response.json()["role"] == "admin"


@patch("app.router.admin.mongodb.db", new={})
@patch("app.router.admin.UserService")
def test_member_cannot_access_admin_endpoint(mock_user_service):
    mock_user_service.return_value.check_admin_access.side_effect = (
        AdminAccessRequiredException()
    )

    response = client.get(
        "/users/admin-only",
        params={"email": "member@example.com"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@patch("app.router.admin.mongodb.db", new={})
@patch("app.router.admin.UserService")
def test_user_not_found(mock_user_service):
    mock_user_service.return_value.check_admin_access.side_effect = (
        UserNotFoundException()
    )

    response = client.get(
        "/users/admin-only",
        params={"email": "missing@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_invalid_email():
    response = client.get(
        "/users/admin-only",
        params={"email": "invalid-email"},
    )

    assert response.status_code == 422