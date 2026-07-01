import base64

from app.exceptions.user_exceptions import (
    UserAlreadyExistsException,
    InvalidPasswordEncodingException,
    InvalidCredentialsException,
)
from app.exceptions.user_exceptions import (
    UserNotFoundException,
    AdminAccessRequiredException,
)

from app.models.user_model import user_model
from app.utils.security import hash_password, verify_password


class UserService:

    def __init__(self, db):
        self.collection = db["users"]

    def create_user(self, user_data):
        # Check duplicate email
        existing_user = self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise UserAlreadyExistsException()

        # Decode Base64 password sent from frontend
        try:
            decoded_password = base64.b64decode(user_data.password).decode("utf-8")
        except Exception:
            raise InvalidPasswordEncodingException()

        # Hash decoded password
        hashed_password = hash_password(decoded_password)

        new_user = user_model(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )

        result = self.collection.insert_one(new_user)

        return str(result.inserted_id)

    def login_user(self, login_data):
        user = self.collection.find_one({"email": login_data.email})

        if not user:
            raise InvalidCredentialsException()

        try:
            decoded_password = base64.b64decode(login_data.password).decode("utf-8")
        except Exception:
            raise InvalidPasswordEncodingException()

        is_password_valid = verify_password(
            decoded_password,
            user["password"]
        )

        if not is_password_valid:
            raise InvalidCredentialsException()

        return {
            "user_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }

    def check_admin_access(self, email: str):
        user = self.collection.find_one({"email": email})

        if not user:
            raise UserNotFoundException()

        if user["role"] != "admin":
            raise AdminAccessRequiredException()

        return {
            "email": user["email"],
            "role": user["role"]
        }

    def get_users_by_role(self, role: str):
        users = self.collection.find({"role": role})

        return [
        {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
        }
        for user in users
    ]