from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import get_db
from app.exceptions.user_exceptions import (
    AdminAccessRequiredException,
    UserNotFoundException,
)
from main import app

client = TestClient(app)


def override_get_db():
    return {}


app.dependency_overrides[get_db] = override_get_db


@patch("app.router.admin.UserService")
def test_admin_can_access_admin_endpoint(mock_user_service):
    mock_user_service.return_value.check_admin_access.return_value = {
        "_id": "507f1f77bcf86cd799439012",
        "email": "admin@gmail.com",
        "role": "admin",
    }

    response = client.get(
        "/users/admin-only",
        params={"user_id": "507f1f77bcf86cd799439012"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Admin access granted"
    assert response.json()["role"] == "admin"


@patch("app.router.admin.UserService")
def test_member_cannot_access_admin_endpoint(mock_user_service):
    mock_user_service.return_value.check_admin_access.side_effect = (
        AdminAccessRequiredException()
    )

    response = client.get(
        "/users/admin-only",
        params={"user_id": "507f1f77bcf86cd799439013"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


@patch("app.router.admin.UserService")
def test_user_not_found(mock_user_service):
    mock_user_service.return_value.check_admin_access.side_effect = (
        UserNotFoundException()
    )

    response = client.get(
        "/users/admin-only",
        params={"user_id": "507f1f77bcf86cd799439014"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_missing_user_id():
    response = client.get("/users/admin-only")

    assert response.status_code == 422