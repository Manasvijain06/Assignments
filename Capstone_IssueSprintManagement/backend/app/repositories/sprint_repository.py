from bson import ObjectId


from app.constants.collections import (
    ISSUES_COLLECTION,
    PROJECTS_COLLECTION,
    SPRINTS_COLLECTION,
)


class SprintRepository:
    """
    Repository layer for sprint collection.
    """

    def __init__(self, db):
        self.sprints_collection = db[SPRINTS_COLLECTION]
        self.issues_collection = db[ISSUES_COLLECTION]
        self.projects_collection = db[PROJECTS_COLLECTION]

    def find_project_by_id(self, project_id: ObjectId):
        return self.projects_collection.find_one({"_id": project_id})

    def find_issue_by_id(self, issue_id: ObjectId):
        return self.issues_collection.find_one({"_id": issue_id})

    def create_sprint(self, sprint: dict):
        return self.sprints_collection.insert_one(sprint)

    def find_sprint_by_id(self, sprint_id: ObjectId):
        return self.sprints_collection.find_one({"_id": sprint_id})

    def add_issue_to_sprint(self, sprint_id: ObjectId, issue_id: ObjectId, updated_at):
        return self.sprints_collection.update_one(
            {"_id": sprint_id},
            {
                "$addToSet": {"issues": issue_id},
                "$set": {"updated_at": updated_at},
            },
        )

    def remove_issue_from_sprint(self, sprint_id: ObjectId, issue_id: ObjectId, updated_at):
        return self.sprints_collection.update_one(
            {"_id": sprint_id},
            {
                "$pull": {"issues": issue_id},
                "$set": {"updated_at": updated_at},
            },
        )

    def get_sprints(self, query: dict, page: int, limit: int):
        skip = (page - 1) * limit

        return list(
            self.sprints_collection.find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )


    def count_sprints(self, query: dict):
        return self.sprints_collection.count_documents(query)


    def find_issues_by_ids(self, issue_ids: list):
        return list(self.issues_collection.find({"_id": {"$in": issue_ids}}))

    def find_by_name(self, project_id: ObjectId, name: str):
        return self.sprints_collection.find_one(
            {
                "project_id": project_id,
                "name": {
                    "$regex": f"^{name}$",
                    "$options": "i",
                },
            }
        )

    def update_sprint_status(self, sprint_id: ObjectId, status: str, updated_at):
        return self.sprints_collection.update_one(
            {"_id": sprint_id},
            {
                "$set": {
                    "status": status,
                    "updated_at": updated_at,
                }
            },
        )

    def find_sprint_by_issue(self, issue_id: ObjectId):
        return self.sprints_collection.find_one({
            "issues": issue_id
        })

    def find_active_sprint_by_project(self, project_id: ObjectId):
        return self.sprints_collection.find_one(
            {
                "project_id": project_id,
                "status": "active",
            }
        )