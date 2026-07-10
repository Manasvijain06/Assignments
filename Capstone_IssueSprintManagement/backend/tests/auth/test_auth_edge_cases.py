import base64
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.dependencies.database import get_db
from app.exceptions.user_exceptions import InvalidCredentialsException
from main import app

client = TestClient(app)


def override_get_db():
    return {}


app.dependency_overrides[get_db] = override_get_db


def encode_password(password: str) -> str:
    return base64.b64encode(password.encode()).decode()


def test_register_invalid_role():
    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "manasvi@gmail.com",
            "password": encode_password("Password123!"),
            "role": "superadmin",
        },
    )

    assert response.status_code == 422


def test_register_weak_password():
    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "manasvi@gmail.com",
            "password": encode_password("weak"),
            "role": "member",
        },
    )

    assert response.status_code == 422


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