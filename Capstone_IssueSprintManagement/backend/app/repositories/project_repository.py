from bson import ObjectId


class ProjectRepository:
    """
    Handles all database operations related to projects.
    """

    def __init__(self, db):
        self.collection = db["projects"]

    def create_project(self, project: dict):
        """
        Insert a new project document.
        """
        return self.collection.insert_one(project)

    def find_by_id(self, project_id: ObjectId):
        """
        Find project by MongoDB ObjectId.
        """
        return self.collection.find_one({"_id": project_id})

    def find_by_key(self, project_key: str):
        """
        Find project by unique project key.
        """
        return self.collection.find_one({"project_key": project_key.upper()})

    def get_all_projects(self):
        """
        Fetch all projects.
        """
        return self.collection.find()

    def update_description(self, project_id: ObjectId, description: str):
        """
        Update only project description.
        """
        return self.collection.update_one(
            {"_id": project_id},
            {"$set": {"description": description}},
        )

    def add_member(self, project_id: ObjectId, member_id: ObjectId):
        """
        Add a member to project.
        """
        return self.collection.update_one(
            {"_id": project_id},
            {"$addToSet": {"members": member_id}},
        )

    def remove_member(self, project_id: ObjectId, member_id: ObjectId):
        """
        Remove a member from project.
        """
        return self.collection.update_one(
            {"_id": project_id},
            {"$pull": {"members": member_id}},
        )

    def delete_project(self, project_id: ObjectId):
        """
        Delete project by ID.
        """
        return self.collection.delete_one({"_id": project_id})