from datetime import UTC, datetime

from bson import ObjectId


class SprintModel:
    """
    Sprint document model.
    """

    @staticmethod
    def build(
        name: str,
        project_id: str,
        created_by: str,
        start_date,
        end_date,
    ) -> dict:
        """
        Build a sprint document for MongoDB
        """
        now = datetime.now(UTC)

        return {
            "name": name,
            "project_id": ObjectId(project_id),
            "created_by": ObjectId(created_by),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "issues": [],
            "status": "planned",
            "created_at": now,
            "updated_at": now,
        }