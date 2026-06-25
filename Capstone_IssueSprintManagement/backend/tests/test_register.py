from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_invalid_email():
    response = client.post(
        "/auth/register",
        json={
            "name": "Manasvi",
            "email": "invalid-email",
            "password": "Password123",
            "role": "member"
        }
    )

    assert response.status_code == 422