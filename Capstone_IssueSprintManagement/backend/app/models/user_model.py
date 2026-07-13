from datetime import UTC, datetime

class UserModel:
    """
    User document model.
    """

    @staticmethod
    def build(
        name: str,
        email: str,
        hashed_password: str,
        role: str,
    ) -> dict:
        """
        Build a user document for MongoDB.
        """
        now = datetime.now(UTC)

        return {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role,
            "created_at": now,
            "updated_at": now
    }