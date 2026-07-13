from bson import ObjectId
from app.constants.collections import USERS_COLLECTION

class UserRepository:
    """
    Repository layer for User collection.
    """

    def __init__(self, db):
        self.collection = db[USERS_COLLECTION]

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
        Return all users of a specific role.
        """
        return list(
            self.collection.find({"role": role})
        )


    def update_password(self, user_id: str, hashed_password: str):
        """
        Update the user's password.
        """
        return self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed_password}},
        )