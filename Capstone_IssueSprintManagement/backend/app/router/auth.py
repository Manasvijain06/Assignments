from fastapi import APIRouter, HTTPException

from app.database import mongodb
from app.exceptions.user_exceptions import (
    UserAlreadyExistsException,
    InvalidPasswordEncodingException,
    InvalidCredentialsException,
)
from app.schemas.requests.auth_request import (
    UserRegisterRequest,
    UserLoginRequest,
)
from app.schemas.responses.auth_response import (
    UserRegisterResponse,
    UserLoginResponse
)
from app.services.user_service import UserService


router = APIRouter()

@router.post("/register", response_model=UserRegisterResponse)
def register_user(user: UserRegisterRequest):
    """
    Register a new user.
    """
    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )

    try:
        user_service = UserService(mongodb.db)
        user_id = user_service.create_user(user)

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }

    except UserAlreadyExistsException as exc:
        raise HTTPException(status_code=409, detail=exc.message)

    except InvalidPasswordEncodingException as exc:
        raise HTTPException(status_code=400, detail=exc.message)


@router.post("/login", response_model=UserLoginResponse)
def login_user(user: UserLoginRequest):
    """
    Login a user and return user details."""

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )

    try:
        user_service = UserService(mongodb.db)
        logged_in_user = user_service.login_user(user)

        return {
            "message": "Login successful",
            **logged_in_user,
        }

    except InvalidCredentialsException as exc:
        raise HTTPException(status_code=401, detail=exc.message)

    except InvalidPasswordEncodingException as exc:
        raise HTTPException(status_code=400, detail=exc.message)