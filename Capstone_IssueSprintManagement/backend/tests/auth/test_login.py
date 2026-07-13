import base64
from unittest.mock import patch

from app.dependencies.database import get_db
from fastapi.testclient import TestClient
from main import app
from app.exceptions.user_exceptions import InvalidCredentialsException

client = TestClient(app)

def override_get_db():
    return {}


app.dependency_overrides[get_db] = override_get_db

def encode_password(password: str) -> str:
    return base64.b64encode(password.encode()).decode()


@patch("app.router.auth.UserService")
def test_login_success(mock_user_service):
    mock_user_service.return_value.login_user.return_value = {
        "user_id": "mock_user_id",
        "name": "Manasvi",
        "email": "manasvi@gmail.com",
        "role": "member",
        "access_token": "mock_token",
        "token_type": "bearer",
    }

    response = client.post(
        "/auth/login",
        json={
            "email": "manasvi@gmail.com",
            "password": encode_password("Password123!"),
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert response.json()["user_id"] == "mock_user_id"
    assert response.json()["email"] == "manasvi@gmail.com"
    assert response.json()["role"] == "member"


@patch("app.router.auth.UserService")
def test_login_invalid_credentials(mock_user_service):
    mock_user_service.return_value.login_user.side_effect = (
        InvalidCredentialsException()
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "manasvi@gmail.com",
            "password": encode_password("WrongPassword123!"),
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_invalid_email():
    response = client.post(
        "/auth/login",
        json={
            "email": "invalid-email",
            "password": encode_password("Password123!"),
        },
    )

    assert response.status_code == 422