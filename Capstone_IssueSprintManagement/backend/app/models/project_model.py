from datetime import datetime, UTC

from bson import ObjectId

class ProjectModel:

    @staticmethod
    def build(
        name: str,
        description: str,
        project_key: str,
        members: list,
        created_by: str,
    ) -> dict:
        """
        Build a project document for MongoDB.
        """
        now = datetime.now(UTC)


        return {
            "name": name,
            "description": description,
            "project_key": project_key.upper(),
            "members": [ObjectId(member) for member in members],
            "created_by": ObjectId(created_by),
            "created_at": now,
            "updated_at": now
    }