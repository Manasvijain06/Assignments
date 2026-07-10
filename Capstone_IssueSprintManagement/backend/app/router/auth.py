from fastapi import APIRouter, Depends

from app.dependencies.database import get_db
from app.schemas.requests.auth_request import (
    UserRegisterRequest,
    UserLoginRequest,
)
from app.schemas.responses.auth_response import (
    UserRegisterResponse,
    UserLoginResponse,
)
from app.services.user_service import UserService


router = APIRouter()

@router.post("/register", response_model=UserRegisterResponse)
def register_user(user: UserRegisterRequest, db=Depends(get_db)):
    """
    Register a new user.
    """
    user_service = UserService(db)
    user_id = user_service.create_user(user)

    return {
        "message": "User registered successfully",
        "user_id": user_id
    }


@router.post("/login", response_model=UserLoginResponse)
def login_user(user: UserLoginRequest, db=Depends(get_db)):
    """
    Login a user and return user details.
    """
    user_service = UserService(db)
    logged_in_user = user_service.login_user(user)

    return {
        "message": "Login successful",
        **logged_in_user,
    }
