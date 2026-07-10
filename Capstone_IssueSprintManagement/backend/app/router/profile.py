from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException

from app.constants.collections import USERS_COLLECTION
from app.dependencies.database import get_db
from app.schemas.requests.profile_request import (
    UpdateProfileRequest,
    ChangePasswordRequest,
)
from app.utils.security import hash_password, verify_password

router = APIRouter()


def get_user_object_id(user_id: str):
    """
    Convert user id into MongoDB ObjectId.
    """
    try:
        return ObjectId(user_id)
    except InvalidId as exc:
        raise HTTPException(status_code=400, detail="Invalid user id") from exc


@router.put("/{user_id}")
def update_profile(user_id: str, request: UpdateProfileRequest, db=Depends(get_db)):
    """
    Update user profile.
    """
    user_object_id = get_user_object_id(user_id)
    users_collection = db[USERS_COLLECTION]

    user = users_collection.find_one({"_id": user_object_id})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    users_collection.update_one(
        {"_id": user_object_id},
        {"$set": {"name": request.name}},
    )

    return {
        "message": "Profile updated successfully.",
        "user": {
            "user_id": user_id,
            "name": request.name,
            "email": user["email"],
            "role": user["role"],
        },
    }


@router.put("/{user_id}/password")
def change_password(user_id: str, request: ChangePasswordRequest, db=Depends(get_db)):
    """
    Change user password.
    """
    user_object_id = get_user_object_id(user_id)
    users_collection = db[USERS_COLLECTION]

    user = users_collection.find_one({"_id": user_object_id})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(request.current_password, user["password"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    users_collection.update_one(
        {"_id": user_object_id},
        {"$set": {"password": hash_password(request.new_password)}},
    )

    return {"message": "Password changed successfully."}