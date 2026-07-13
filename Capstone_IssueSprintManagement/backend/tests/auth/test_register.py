from unittest.mock import patch

from fastapi.testclient import TestClient

from app.exceptions.user_exceptions import UserAlreadyExistsException
from main import app

client = TestClient(app)


@patch("app.router.auth.UserService")
def test_register_success(mock_user_service):
    mock_user_service.return_value.create_user.return_value = "mock_user_id"

    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "manasvi@gmail.com",
            "password": "Password123!",
            "role": "member",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "User registered successfully",
        "user_id": "mock_user_id",
    }

    mock_user_service.return_value.create_user.assert_called_once()


@patch("app.router.auth.UserService")
def test_register_duplicate_email(mock_user_service):
    mock_user_service.return_value.create_user.side_effect = (
        UserAlreadyExistsException()
    )

    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "manasvi@gmail.com",
            "password": "Password123!",
            "role": "member",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_register_invalid_email():
    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "invalid-email",
            "password": "Password123!",
            "role": "member",
        },
    )

    assert response.status_code == 422


def test_register_invalid_password():
    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "manasvi@gmail.com",
            "password": "password",
            "role": "member",
        },
    )

    assert response.status_code == 422


def test_register_missing_fields():
    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
        },
    )

    assert response.status_code == 422