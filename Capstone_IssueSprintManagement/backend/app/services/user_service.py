import base64

from app.exceptions.user_exceptions import (
    UserAlreadyExistsException,
    InvalidPasswordEncodingException,
)

from app.models.user_model import user_model
from app.utils.security import hash_password


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