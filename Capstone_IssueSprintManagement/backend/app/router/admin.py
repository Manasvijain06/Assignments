from fastapi import APIRouter, HTTPException, Query
from pydantic import EmailStr

from app.database import mongodb
from app.exceptions.user_exceptions import (
    UserNotFoundException,
    AdminAccessRequiredException,
)
from app.schemas.user_schema import AdminAccessResponse
from app.services.user_service import UserService

router = APIRouter()


@router.get("/admin-only", response_model=AdminAccessResponse)
def admin_only_endpoint(email: EmailStr = Query(...)):

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )

    try:
        user_service = UserService(mongodb.db)
        user = user_service.check_admin_access(email)

        return {
            "message": "Admin access granted",
            "email": user["email"],
            "role": user["role"]
        }

    except UserNotFoundException as exc:
        raise HTTPException(status_code=404, detail=exc.message)

    except AdminAccessRequiredException as exc:
        raise HTTPException(status_code=403, detail=exc.message)