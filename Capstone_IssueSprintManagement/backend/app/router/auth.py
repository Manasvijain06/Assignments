from fastapi import APIRouter, HTTPException

from app.schemas.user_schema import UserRegister, UserRegisterResponse
from app.database import mongodb
from app.services.user_service import UserService
from app.exceptions.user_exceptions import (
    UserAlreadyExistsException,
    InvalidPasswordEncodingException,
)

router = APIRouter()

@router.post("/register", response_model=UserRegisterResponse)
def register_user(user: UserRegister):

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
        raise HTTPException(
            status_code=409,
            detail=exc.message
        )

    except InvalidPasswordEncodingException as exc:
        raise HTTPException(
            status_code=400,
            detail=exc.message
        )