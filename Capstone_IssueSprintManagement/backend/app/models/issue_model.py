from datetime import UTC, datetime
from bson import ObjectId


class IssueModel:
    """
    Issue document model.
    """

    @staticmethod
    def build(
        project_id: str,
        issue_key: str,
        title: str,
        description: str,
        issue_type: str,
        priority: str,
        created_by: str,
        assignee: str,
        parent_id: str | None = None,
    ):
        current_time = datetime.now(UTC)

        return {
            "project_id": ObjectId(project_id),
            "issue_key": issue_key,
            "title": title,
            "description": description,
            "type": issue_type,
            "priority": priority,
            "status": "backlog",
            "created_by": ObjectId(created_by),
            "assignee": ObjectId(assignee),
            "parent_id": ObjectId(parent_id) if parent_id else None,
            "created_at": current_time,
            "updated_at": current_time,
        }