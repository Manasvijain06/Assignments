from unittest.mock import patch

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.dependencies.authentication import get_current_user
from app.dependencies.database import get_db
from app.exceptions.user_exceptions import UserNotFoundException
from main import app


ADMIN_ID = "507f1f77bcf86cd799439012"
MEMBER_ID = "507f1f77bcf86cd799439013"

client = TestClient(app)


def override_get_db():
    """
    Return a fake database for router-level tests.
    """
    return {}


def override_admin_user():
    """
    Return a mock authenticated admin.
    """
    return {
        "_id": ObjectId(ADMIN_ID),
        "name": "Admin User",
        "email": "admin@gmail.com",
        "role": "admin",
    }


def override_member_user():
    """
    Return a mock authenticated member.
    """
    return {
        "_id": ObjectId(MEMBER_ID),
        "name": "Member User",
        "email": "member@gmail.com",
        "role": "member",
    }


@pytest.fixture(autouse=True)
def override_dependencies():
    """
    Reset and apply required dependencies before every test.
    """
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_admin_user

    yield

    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_current_user, None)


@patch("app.router.admin.UserService")
def test_admin_can_access_admin_endpoint(mock_user_service):
    mock_user_service.return_value.check_admin_access.return_value = {
        "_id": ObjectId(ADMIN_ID),
        "email": "admin@gmail.com",
        "role": "admin",
    }

    response = client.get("/users/admin-only")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Admin access granted"
    assert data["user_id"] == ADMIN_ID
    assert data["email"] == "admin@gmail.com"
    assert data["role"] == "admin"

    mock_user_service.return_value.check_admin_access.assert_called_once_with(
        ADMIN_ID
    )


@patch("app.router.admin.UserService")
def test_member_cannot_access_admin_endpoint(mock_user_service):
    app.dependency_overrides[get_current_user] = override_member_user

    response = client.get("/users/admin-only")

    assert response.status_code == 403

    assert response.json()["detail"] in {
        "Admin access required",
        "Admin access required.",
        "You are not allowed to perform this action.",
        "You are not authorized to perform this action.",
    }

    mock_user_service.return_value.check_admin_access.assert_not_called()


@patch("app.router.admin.UserService")
def test_user_not_found(mock_user_service):
    mock_user_service.return_value.check_admin_access.side_effect = (
        UserNotFoundException()
    )

    response = client.get("/users/admin-only")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_admin_endpoint_without_token():
    app.dependency_overrides.pop(get_current_user, None)

    response = client.get("/users/admin-only")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"