from typing import List

from fastapi import APIRouter, HTTPException, Query

from app.database import mongodb
from app.exceptions.user_exceptions import (
    AdminAccessRequiredException,
    UserNotFoundException,
)
from app.schemas.responses.auth_response import (
    AdminAccessResponse,
    UserListResponse,
)
from app.services.user_service import UserService

router = APIRouter()


@router.get("/admin-only", response_model=AdminAccessResponse)
def admin_only_endpoint(user_id: str = Query(...)):
    """
    Check whether the given user has Admin access.
    """

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )

    try:
        user_service = UserService(mongodb.db)
        user = user_service.check_admin_access(user_id)

        return {
            "message": "Admin access granted",
            "user_id": str(user["_id"]),
            "email": user["email"],
            "role": user["role"]
        }
    except UserNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)

    except AdminAccessRequiredException as exc:
        raise HTTPException(status_code=403, detail=exc.message)


@router.get("/by-role", response_model=List[UserListResponse])
def get_users_by_role(role: str = Query(...)):
    """
    Fetch users by role.
    """

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )

    user_service = UserService(mongodb.db)

    return user_service.get_users_by_role(role)