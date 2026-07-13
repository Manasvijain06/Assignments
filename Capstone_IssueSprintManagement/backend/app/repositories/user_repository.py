from bson import ObjectId


class UserRepository:
    """
    Repository layer for User collection.
    Handles all database operations related to users.
    """

    def __init__(self, db):
        self.collection = db["users"]

    def create_user(self, user: dict):
        """
        Insert a new user document.
        """
        return self.collection.insert_one(user)

    def find_by_email(self, email: str):
        """
        Find a user by email.
        """
        return self.collection.find_one({"email": email})

    def find_by_id(self, user_id: str):
        """
        Find a user using MongoDB ObjectId.
        """
        return self.collection.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )

    def get_users_by_role(self, role: str):
        """
        Get all users of a specific role.
        """
        return list(
            self.collection.find(
                {"role": role}
            )
        )