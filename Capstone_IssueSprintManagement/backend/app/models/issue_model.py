from datetime import UTC, datetime
from bson import ObjectId


class IssueModel:
    """
    Issue document model.
    """

    @staticmethod
    def build(
        project_id: str,
        title: str,
        description: str,
        created_by: str,
    ) -> dict:
        current_time = datetime.now(UTC)

        return {
            "project_id": ObjectId(project_id),
            "title": title,
            "description": description,
            "created_by": ObjectId(created_by),
            "status": "todo",
            "created_at": current_time,
            "updated_at": current_time,
        }