from app.utils.security import hash_password


class UserService:

    def __init__(self, db):
        self.collection = db["users"]

    def create_user(self, user_data):
        # check duplicate email
        if self.collection.find_one({"email": user_data.email}):
            return None

        hashed_pwd = hash_password(user_data.password)

        user_dict = user_data.model_dump()
        user_dict["password"] = hashed_pwd

        result = self.collection.insert_one(user_dict)

        return str(result.inserted_id)