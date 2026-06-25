from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserRegister
from app.database.mongodb import users_collection
from app.utils.security import hash_password

router = APIRouter()

@router.post("/register")
def register_user(user: UserRegister):

    # check if user already exists
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # hash password
    hashed_pw = hash_password(user.password)

    # create user document
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pw,
        "role": user.role
    }

    result = users_collection.insert_one(user_data)

    return {"message": "User registered successfully",
            "user_id": str(result.inserted_id)
            }