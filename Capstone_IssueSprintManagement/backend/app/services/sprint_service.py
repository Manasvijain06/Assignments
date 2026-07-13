from datetime import UTC, datetime
import math

from bson import ObjectId
from bson.errors import InvalidId

from app.exceptions.project_exceptions import ProjectNotFoundException
from app.exceptions.sprint_exceptions import (
    DoneIssueCannotBeAddedException,
    IssueAlreadyInSprintException,
    SprintCreationFailedException,
    SprintNotFoundException,
    SprintAlreadyExistsException,
)
from app.exceptions.user_exceptions import UserNotFoundException
from app.models.sprint_model import SprintModel
from app.repositories.sprint_repository import SprintRepository
from app.repositories.user_repository import UserRepository


class SprintService:
    """
    Business logic layer for sprint management.
    """

    def __init__(self, db):
        self.sprint_repository = SprintRepository(db)
        self.user_repository = UserRepository(db)

    def _get_object_id(self, object_id: str):
        try:
            return ObjectId(object_id)
        except InvalidId:
            raise SprintNotFoundException()

    def create_sprint(self, sprint_data):
        project_id = self._get_object_id(sprint_data.project_id)
        created_by = self.user_repository.find_by_id(sprint_data.created_by)

        if not self.sprint_repository.find_project_by_id(project_id):
            raise ProjectNotFoundException()

        existing_sprint = self.sprint_repository.find_by_name(
            project_id,
            sprint_data.name,
        )

        if existing_sprint:
            raise SprintAlreadyExistsException()

        if not created_by:
            raise UserNotFoundException()

        sprint = SprintModel.build(
            name=sprint_data.name,
            project_id=sprint_data.project_id,
            created_by=sprint_data.created_by,
            start_date=sprint_data.start_date,
            end_date=sprint_data.end_date,
        )

        result = self.sprint_repository.create_sprint(sprint)

        if not result.inserted_id:
            raise SprintCreationFailedException()

        return str(result.inserted_id)

    def add_issue_to_sprint(self, sprint_id: str, issue_id: str):
        sprint_object_id = self._get_object_id(sprint_id)
        issue_object_id = self._get_object_id(issue_id)

        sprint = self.sprint_repository.find_sprint_by_id(sprint_object_id)

        if not sprint:
            raise SprintNotFoundException()

        issue = self.sprint_repository.find_issue_by_id(issue_object_id)

        if not issue:
            raise SprintNotFoundException("Issue not found")

        if issue["status"] == "done":
            raise DoneIssueCannotBeAddedException()

        if issue_object_id in sprint.get("issues", []):
            raise IssueAlreadyInSprintException()

        self.sprint_repository.add_issue_to_sprint(
            sprint_object_id,
            issue_object_id,
            datetime.now(UTC),
        )

    def remove_issue_from_sprint(self, sprint_id: str, issue_id: str):
        sprint_object_id = self._get_object_id(sprint_id)
        issue_object_id = self._get_object_id(issue_id)

        sprint = self.sprint_repository.find_sprint_by_id(sprint_object_id)

        if not sprint:
            raise SprintNotFoundException()

        self.sprint_repository.remove_issue_from_sprint(
            sprint_object_id,
            issue_object_id,
            datetime.now(UTC),
        )

    def _calculate_sprint_status(self, start_date, end_date):
        today = datetime.now(UTC).date()

        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date).date()

        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date).date()

        if today < start_date:
            return "planned"

        if start_date <= today <= end_date:
            return "active"

        return "completed"


    def _format_sprint(self, sprint):
        sprint_issues = self.sprint_repository.find_issues_by_ids(
            sprint.get("issues", [])
        )

        total_issues = len(sprint_issues)

        completed_issues = len([
            issue for issue in sprint_issues
            if issue.get("status") == "done"
        ])

        progress = int((completed_issues / total_issues) * 100) if total_issues else 0

        return {
            "sprint_id": str(sprint["_id"]),
            "name": sprint["name"],
            "project_id": str(sprint["project_id"]),
            "status": self._calculate_sprint_status(
                sprint["start_date"],
                sprint["end_date"],
            ),
            "start_date": str(sprint["start_date"]),
            "end_date": str(sprint["end_date"]),
            "total_issues": total_issues,
            "completed_issues": completed_issues,
            "progress": progress,
            "issues": [
                {
                    "issue_id": str(issue["_id"]),
                    "issue_key": issue.get("issue_key", ""),
                    "title": issue.get("title", ""),
                    "status": issue.get("status", ""),
                    "type": issue.get("type", ""),
                }
                for issue in sprint_issues
            ],
        }


    def get_sprints(
        self,
        page: int,
        limit: int,
        project_id: str | None,
        status: str | None,
        search: str | None,
    ):
        query = {}

        if project_id and project_id != "all":
            query["project_id"] = ObjectId(project_id)

        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        total = self.sprint_repository.count_sprints(query)

        sprints = self.sprint_repository.get_sprints(
            query,
            page,
            limit,
        )

        formatted_sprints = [
            self._format_sprint(sprint)
            for sprint in sprints
        ]

        if status and status != "all":
            formatted_sprints = [
                sprint for sprint in formatted_sprints
                if sprint["status"] == status
            ]

        return {
            "items": formatted_sprints,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": math.ceil(total / limit) if total else 1,
        }