from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserRegister, UserLogin
from app.database.mongodb import users_collection
from app.utils.security import hash_password
from app.utils.security import verify_password
from app.utils.jwt_handler import create_access_token
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
# login
@router.post("/login")
def login_user(user: UserLogin):

    db_user = users_collection.find_one(
        {"email": user.email}
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "user_id": str(db_user["_id"]),
        "email": db_user["email"],
        "role": db_user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }