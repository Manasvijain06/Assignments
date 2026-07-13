from bson import ObjectId
from app.constants.collections import PROJECTS_COLLECTION

class ProjectRepository:
    """
    Handles all database operations related to projects.
    """

    def __init__(self, db):
        self.collection = db[PROJECTS_COLLECTION]

    def create_project(self, project: dict):
        return self.collection.insert_one(project)

    def find_by_id(self, project_id: ObjectId):
        return self.collection.find_one({"_id": project_id})

    def find_by_key(self, project_key: str):
        return self.collection.find_one({"project_key": project_key.upper()})

    def get_all_projects(self, page: int, limit: int):
        skip = (page - 1) * limit

        return(
            self.collection
            .find({})
            .skip(skip)
            .limit(limit)
        )

    def count_projects(self):
        return self.collection.count_documents({})

    def update_description(self, project_id: ObjectId, description: str):
        return self.collection.update_one(
            {"_id": project_id},
            {"$set": {"description": description}},
        )

    def add_member(self, project_id: ObjectId, member_id: ObjectId):
        return self.collection.update_one(
            {"_id": project_id},
            {"$addToSet": {"members": member_id}},
        )

    def remove_member(self, project_id: ObjectId, member_id: ObjectId):
        return self.collection.update_one(
            {"_id": project_id},
            {"$pull": {"members": member_id}},
        )

    def delete_project(self, project_id: ObjectId):
        return self.collection.delete_one({"_id": project_id})