from bson import ObjectId
from bson.errors import InvalidId

from app.exceptions.project_exceptions import ProjectNotFoundException
from app.exceptions.user_exceptions import UserNotFoundException
from app.models.issue_model import IssueModel
from app.repositories.issue_repository import IssueRepository
from app.repositories.user_repository import UserRepository


class IssueService:
    """
    Business logic layer for issue management.
    """

    def __init__(self, db):
        self.issue_repository = IssueRepository(db)
        self.user_repository = UserRepository(db)

    def _get_object_id(self, object_id: str):
        try:
            return ObjectId(object_id)
        except InvalidId:
            raise ProjectNotFoundException()

    def create_issue(self, project_id: str, issue_data):
        project_object_id = self._get_object_id(project_id)

        project = self.issue_repository.find_project_by_id(project_object_id)

        if not project:
            raise ProjectNotFoundException()

        creator = self.user_repository.find_by_id(issue_data.created_by)

        if not creator:
            raise UserNotFoundException()

        issue = IssueModel.build(
            project_id=project_id,
            title=issue_data.title,
            description=issue_data.description,
            created_by=issue_data.created_by,
        )

        result = self.issue_repository.create_issue(issue)

        return str(result.inserted_id)