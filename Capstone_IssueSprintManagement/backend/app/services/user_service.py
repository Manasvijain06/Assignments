import base64

from app.exceptions.user_exceptions import (
    UserAlreadyExistsException,
    InvalidPasswordEncodingException,
    InvalidCredentialsException,
    UserNotFoundException,
    AdminAccessRequiredException,
    SamePasswordException,
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

        hashed_password = hash_password(user_data.password)

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

        if not verify_password(login_data.password, user["password"]):
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


    def login_plain_password(self, email: str, password: str):
        """
        Authenticate a user using a plain password for Swagger.
        """
        user = self.user_repository.find_by_email(email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(password, user["password"]):
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

    def change_password(self, user_id: str, password_data):
        """
        Change the user's password.
        """
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        current_password = password_data.current_password
        new_password = password_data.new_password

        if not verify_password(current_password, user["password"]):
            raise InvalidCredentialsException()

        if verify_password(new_password, user["password"]):
            raise SamePasswordException()

        hashed_password = hash_password(new_password)

        self.user_repository.update_password(
            user_id,
            hashed_password,
        )