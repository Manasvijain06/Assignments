import base64

from app.exceptions.user_exceptions import (
    UserAlreadyExistsException,
    InvalidPasswordEncodingException,
    InvalidCredentialsException,
    UserNotFoundException,
    AdminAccessRequiredException,
)

from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.utils.jwt_handler import create_access_token
from app.utils.security import hash_password, verify_password


class UserService:
    """
    Business logic for user management.
    """
    def __init__(self, db):
        self.user_repository = UserRepository(db)

    def create_user(self, user_data):
        """
        Register a new user.
        """
        existing_user = self.user_repository.find_by_email(user_data.email)

        if existing_user:
            raise UserAlreadyExistsException()

        decoded_password = self.decode_password(user_data.password)
        hashed_password = hash_password(decoded_password)

        new_user = UserModel.build(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )

        result = self.user_repository.create_user(new_user)
        return str(result.inserted_id)

    def login_user(self, login_data):
        """
        Authenticate user.
        """
        user = self.user_repository.find_by_email(login_data.email)

        if not user:
            raise InvalidCredentialsException()

        decoded_password = self.decode_password(login_data.password)

        if not verify_password(decoded_password, user["password"]):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            {
                "sub": str(user["_id"]),
                "role": user["role"],
            }
        )
        return {
            "user_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "access_token": access_token,
            "token_type": "bearer",
        }

    def check_admin_access(self, user_id: str):
        """
        Verify whether the user has Admin access.
        """
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        if user["role"] != "admin":
            raise AdminAccessRequiredException()

        return user

    def get_users_by_role(self, role: str):
        """
        Fetch users based on role.
        """
        users = self.user_repository.get_users_by_role(role)

        return [
        {
            "user_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
        }
        for user in users
    ]

    def decode_password(self, password: str):
        """
        Decode Base64 password.
        """
        try:
            return base64.b64decode(password).decode("utf-8")
        except Exception as exc:
            raise InvalidPasswordEncodingException() from exc