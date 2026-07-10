from bson import ObjectId
from datetime import datetime, UTC

from app.constants.collections import ISSUES_COLLECTION, PROJECTS_COLLECTION

class IssueRepository:
    """
    Repository layer for Issue-related database operations.
    """

    def __init__(self, db):
        self.issues_collection = db[ISSUES_COLLECTION]
        self.projects_collection = db[PROJECTS_COLLECTION]

    def find_project_by_id(self, project_id: ObjectId):
        return self.projects_collection.find_one({"_id": project_id})

    def count_project_issues(self, project_id: ObjectId):
        return self.issues_collection.count_documents({"project_id": project_id})

    def create_issue(self, issue: dict):
        return self.issues_collection.insert_one(issue)

    def find_by_id(self, issue_id: ObjectId):
        return self.issues_collection.find_one({"_id": issue_id})

    def find_parent_ids_by_child_search(self, project_id: ObjectId, search: str):
        children = self.issues_collection.find(
            {
                "project_id": project_id,
                "parent_id": {"$ne": None},
                "$or": [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                    {"issue_key": {"$regex": search, "$options": "i"}},
                    {"status": {"$regex": search, "$options": "i"}},
                    {"priority": {"$regex": search, "$options": "i"}},
                    {"type": {"$regex": search, "$options": "i"}},
                ],
            }
        )

        return [child["parent_id"] for child in children if child.get("parent_id")]

    def update_status(self, issue_id: ObjectId, status: str, updated_at):
        return self.issues_collection.update_one(
            {"_id": issue_id},
            {
                "$set": {
                    "status": status,
                    "updated_at": updated_at,
                }
            },
        )

    def get_project_issues(self, query: dict, page: int, limit: int):
        skip = (page - 1) * limit

        return list(
            self.issues_collection
            .find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )

    def count_issues(self, query: dict):
        return self.issues_collection.count_documents(query)

    def get_project_stories(self, project_id: ObjectId):
        return list(
            self.issues_collection.find(
                {
                    "project_id": project_id,
                    "type": "story",
                }
            ).sort("created_at", -1)
        )

    def get_parent_issues(self, query: dict, page: int, limit: int):
        skip = (page - 1) * limit

        parent_filter = {
            "$or": [
                {"parent_id": None},
                {"parent_id": ""},
                {"parent_id": {"$exists": False}},
            ]
        }
        parent_query = {"$and": [query, parent_filter]}

        return list(
            self.issues_collection.find(parent_query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )

    def count_parent_issues(self, query: dict):
        parent_filter = {
            "$or": [
                {"parent_id": None},
                {"parent_id": ""},
                {"parent_id": {"$exists": False}},
            ],
        }

        parent_query = {"$and": [query, parent_filter]}

        return self.issues_collection.count_documents(parent_query)


    def get_child_issues(self, parent_id: ObjectId):
        return list(
            self.issues_collection.find(
                {
                    "$or": [
                        {"parent_id": parent_id},
                        {"parent_id": str(parent_id)},
                    ]
                }
            ).sort("created_at", 1)
        )

    def add_comment(self, issue_id, comment):
        return self.issues_collection.update_one(
            {"_id": issue_id},
            {"$push": {"comments": comment}},
        )

    def update_comment(self, issue_id, comment_id, text):
        return self.issues_collection.update_one(
            {
                "_id": issue_id,
                "comments.comment_id": comment_id,
            },
            {
                "$set": {
                    "comments.$.comment": text,
                    "comments.$.updated_at": datetime.now(UTC),
                }
            },
        )

    def delete_comment(self, issue_id, comment_id):
        return self.issues_collection.update_one(
            {"_id": issue_id},
            {"$pull": {"comments": {"comment_id": comment_id}}},
        )