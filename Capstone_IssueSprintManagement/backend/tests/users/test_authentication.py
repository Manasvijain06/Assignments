from unittest.mock import MagicMock, patch

from bson import ObjectId
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from jose import JWTError

from app.dependencies.authentication import get_current_user


TEST_USER_ID = "507f1f77bcf86cd799439012"

test_app = FastAPI()


@test_app.get("/protected")
def protected_endpoint(
    current_user: dict = Depends(get_current_user),
):
    """
    Test endpoint protected by JWT authentication.
    """
    return {
        "user_id": str(current_user["_id"]),
        "email": current_user["email"],
        "role": current_user["role"],
    }


client = TestClient(test_app)


def create_mock_database(user=None):
    """
    Create a mock MongoDB database and users collection.
    """
    users_collection = MagicMock()
    users_collection.find_one.return_value = user

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = users_collection

    return mock_db, users_collection


def test_protected_endpoint_without_token():
    """
    Request without a Bearer token must return 401.
    """
    response = client.get("/protected")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated",
    }


@patch(
    "app.dependencies.authentication.decode_access_token",
)
def test_valid_token_returns_current_user(
    mock_decode_access_token,
):
    """
    A valid token and existing user should allow access.
    """
    mock_decode_access_token.return_value = {
        "sub": TEST_USER_ID,
        "role": "admin",
    }

    mock_user = {
        "_id": ObjectId(TEST_USER_ID),
        "name": "Admin User",
        "email": "admin@gmail.com",
        "role": "admin",
    }

    mock_db, users_collection = create_mock_database(
        mock_user,
    )

    with patch(
        "app.dependencies.authentication.mongodb.db",
        mock_db,
    ):
        response = client.get(
            "/protected",
            headers={
                "Authorization": "Bearer valid-token",
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": TEST_USER_ID,
        "email": "admin@gmail.com",
        "role": "admin",
    }

    mock_decode_access_token.assert_called_once_with(
        "valid-token",
    )

    users_collection.find_one.assert_called_once_with(
        {
            "_id": ObjectId(TEST_USER_ID),
        }
    )


@patch(
    "app.dependencies.authentication.decode_access_token",
)
def test_invalid_token_returns_401(
    mock_decode_access_token,
):
    """
    An invalid token must return 401.
    """
    mock_decode_access_token.side_effect = JWTError(
        "Invalid token",
    )

    response = client.get(
        "/protected",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials.",
    }


@patch(
    "app.dependencies.authentication.decode_access_token",
)
def test_token_without_subject_returns_401(
    mock_decode_access_token,
):
    """
    A token without the sub claim must return 401.
    """
    mock_decode_access_token.return_value = {
        "role": "admin",
    }

    response = client.get(
        "/protected",
        headers={
            "Authorization": "Bearer token-without-sub",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials.",
    }


@patch(
    "app.dependencies.authentication.decode_access_token",
)
def test_user_not_found_returns_401(
    mock_decode_access_token,
):
    """
    A valid token for a user not found in MongoDB must
    return 401.
    """
    mock_decode_access_token.return_value = {
        "sub": TEST_USER_ID,
        "role": "member",
    }

    mock_db, users_collection = create_mock_database(
        user=None,
    )

    with patch(
        "app.dependencies.authentication.mongodb.db",
        mock_db,
    ):
        response = client.get(
            "/protected",
            headers={
                "Authorization": "Bearer valid-token",
            },
        )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials.",
    }

    users_collection.find_one.assert_called_once_with(
        {
            "_id": ObjectId(TEST_USER_ID),
        }
    )


@patch(
    "app.dependencies.authentication.decode_access_token",
)
def test_database_not_initialized_returns_500(
    mock_decode_access_token,
):
    """
    Return 500 when the database connection is unavailable.
    """
    mock_decode_access_token.return_value = {
        "sub": TEST_USER_ID,
        "role": "admin",
    }

    with patch(
        "app.dependencies.authentication.mongodb.db",
        None,
    ):
        response = client.get(
            "/protected",
            headers={
                "Authorization": "Bearer valid-token",
            },
        )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Database connection not initialized.",
    }