import base64
import uuid
from fastapi.testclient import TestClient
from main import app


def encode_password(password: str) -> str:
    return base64.b64encode(password.encode()).decode()


def test_login_success():
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    password = "Password123!"

    with TestClient(app) as client:
        register_response = client.post(
            "/auth/register",
            json={
                "name": "Login Test User",
                "email": email,
                "password": encode_password(password),
                "role": "member",
            },
        )

        assert register_response.status_code == 200

        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": encode_password(password),
            },
        )

    assert login_response.status_code == 200
    assert login_response.json()["message"] == "Login successful"
    assert login_response.json()["email"] == email
    assert login_response.json()["role"] == "member"
    assert "user_id" in login_response.json()


def test_login_invalid_password():
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"

    with TestClient(app) as client:
        register_response = client.post(
            "/auth/register",
            json={
                "name": "Login Test User",
                "email": email,
                "password": encode_password("Password123!"),
                "role": "member",
            },
        )

        assert register_response.status_code == 200

        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": encode_password("WrongPassword123!"),
            },
        )

    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid email or password"


def test_login_user_not_found():
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={
                "email": f"missing_{uuid.uuid4().hex[:8]}@example.com",
                "password": encode_password("Password123!"),
            },
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_invalid_email():
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={
                "email": "invalid-email",
                "password": encode_password("Password123!"),
            },
        )

    assert response.status_code == 422