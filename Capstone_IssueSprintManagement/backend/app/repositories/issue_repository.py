from bson import ObjectId


class IssueRepository:
    """
    Repository layer for Issue collection.
    """

    def __init__(self, db):
        self.issues_collection = db["issues"]
        self.projects_collection = db["projects"]

    def find_project_by_id(self, project_id: ObjectId):
        return self.projects_collection.find_one({"_id": project_id})

    def create_issue(self, issue: dict):
        return self.issues_collection.insert_one(issue)