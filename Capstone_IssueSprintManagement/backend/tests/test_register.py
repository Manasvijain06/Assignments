import base64
from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app
from app.exceptions.user_exceptions import UserAlreadyExistsException

client = TestClient(app)


def encode_password(password: str) -> str:
    return base64.b64encode(password.encode()).decode()


def test_register_invalid_email():
    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "invalid-email",
            "password": encode_password("Password123!"),
            "role": "member",
        },
    )

    assert response.status_code == 422


@patch("app.router.auth.mongodb.db", new={})
@patch("app.router.auth.UserService")
def test_register_success(mock_user_service):
    mock_user_service.return_value.create_user.return_value = "mock_user_id"

    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "manasvi@example.com",
            "password": encode_password("Password123!"),
            "role": "member",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"
    assert response.json()["user_id"] == "mock_user_id"


@patch("app.router.auth.mongodb.db", new={})
@patch("app.router.auth.UserService")
def test_register_duplicate_email(mock_user_service):
    mock_user_service.return_value.create_user.side_effect = (
        UserAlreadyExistsException()
    )

    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "manasvi@example.com",
            "password": encode_password("Password123!"),
            "role": "member",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"