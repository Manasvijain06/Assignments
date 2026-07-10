from typing import List

from fastapi import APIRouter, Depends, Query

from app.dependencies.database import get_db

from app.schemas.responses.auth_response import (
    AdminAccessResponse,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter()


@router.get("/admin-only", response_model=AdminAccessResponse)
def admin_only_endpoint(user_id: str = Query(...), db=Depends(get_db)):
    """
    Check whether the given user has Admin access.
    """

    user_service = UserService(db)
    user = user_service.check_admin_access(user_id)

    return {
        "message": "Admin access granted",
        "user_id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"],
        }


@router.get("/by-role", response_model=List[UserResponse])
def get_users_by_role(role: str = Query(...), db=Depends(get_db)):
    """
    Fetch users by role.
    """

    user_service = UserService(db)

    return user_service.get_users_by_role(role)