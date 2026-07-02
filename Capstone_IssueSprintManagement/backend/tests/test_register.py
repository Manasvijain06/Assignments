import base64
import uuid
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_register_invalid_email():
    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "invalid-email",
            "password": "UGFzc3dvcmQxMjMh",
            "role": "member"
        }
    )

    assert response.status_code == 422


def test_register_success():
    encoded_password = base64.b64encode("Password123!".encode()).decode()
    unique_email = f"manasvi_{uuid.uuid4().hex[:8]}@example.com"

    with TestClient(app) as client:
        response = client.post(
            "/auth/register",
            json={
                "name": "Manasvi",
                "email": unique_email,
                "password": encoded_password,
                "role": "member",
            },
        )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"
    assert "user_id" in response.json()