import base64
import uuid

from fastapi.testclient import TestClient
from main import app


def encode_password(password: str) -> str:
    return base64.b64encode(password.encode()).decode()


def create_user(client, email: str, role: str):
    return client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": encode_password("Password123!"),
            "role": role,
        },
    )


def test_admin_can_access_admin_endpoint():
    admin_email = f"admin_{uuid.uuid4().hex[:8]}@example.com"

    with TestClient(app) as client:
        create_user(client, admin_email, "admin")

        response = client.get(
            "/users/admin-only",
            params={"email": admin_email}
        )

    assert response.status_code == 200
    assert response.json()["message"] == "Admin access granted"
    assert response.json()["role"] == "admin"


def test_member_cannot_access_admin_endpoint():
    member_email = f"member_{uuid.uuid4().hex[:8]}@example.com"

    with TestClient(app) as client:
        create_user(client, member_email, "member")

        response = client.get(
            "/users/admin-only",
            params={"email": member_email}
        )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_user_not_found():
    with TestClient(app) as client:
        response = client.get(
            "/users/admin-only",
            params={"email": f"missing_{uuid.uuid4().hex[:8]}@example.com"}
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_invalid_email():
    with TestClient(app) as client:
        response = client.get(
            "/users/admin-only",
            params={"email": "invalid-email"}
        )

    assert response.status_code == 422