import math
import uuid
from datetime import UTC, datetime

from bson import ObjectId
from bson.errors import InvalidId

from app.exceptions.issue_exceptions import (
    AssigneeRequiredException,
    InvalidIssueStatusTransitionException,
    IssueNotFoundException,
    InvalidParentIssueException,
    CommentNotFoundException,
    CommentPermissionDeniedException,
)
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
        """
        Convert issue id to ObjectId.
        """
        try:
            return ObjectId(object_id)
        except InvalidId as exc:
            raise IssueNotFoundException() from exc

    def _get_project_object_id(self, project_id: str):
        """
        Convert project id to ObjectId.
        """
        try:
            return ObjectId(project_id)
        except InvalidId as exc:
            raise ProjectNotFoundException() from exc

    def _get_user_details(self, user_id):
        """
        Return formatted user details
        """
        user = self.user_repository.find_by_id(str(user_id))

        if not user:
            return None

        return {
            "user_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
        }

    def create_issue(self, project_id: str, issue_data):
        """
        Create a new issue.
        """
        project_object_id = self._get_project_object_id(project_id)
        project = self.issue_repository.find_project_by_id(project_object_id)

        if not project:
            raise ProjectNotFoundException()

        creator = self.user_repository.find_by_id(issue_data.created_by)
        assignee = self.user_repository.find_by_id(issue_data.assignee)

        if not creator or not assignee:
            raise UserNotFoundException()

        if issue_data.type == "story" and issue_data.parent_id:
            raise InvalidParentIssueException("Story cannot have a parent issue")

        parent_id = self._validate_parent_issue(
            issue_data.parent_id,
            project_object_id,
        )

        issue_count = self.issue_repository.count_project_issues(project_object_id)
        issue_key = f"{project['project_key']}-{issue_count + 1}"

        issue = IssueModel.build(
            project_id=project_id,
            issue_key=issue_key,
            title=issue_data.title,
            description=issue_data.description,
            created_by=issue_data.created_by,
            assignee=issue_data.assignee,
            priority=issue_data.priority,
            issue_type=issue_data.type,
            parent_id=parent_id,
        )

        result = self.issue_repository.create_issue(issue)

        return str(result.inserted_id)

    def _format_issue(self, issue):
        """
        Format issue response.
        """
        parent_story = None

        if issue.get("parent_id"):
            parent = self.issue_repository.find_by_id(issue["parent_id"])

            if parent:
                parent_story = {
                    "issue_id": str(parent["_id"]),
                    "issue_key": parent.get("issue_key", ""),
                    "title": parent.get("title", ""),
                }

        children = self.issue_repository.get_child_issues(issue["_id"])

        return {
            "issue_id": str(issue["_id"]),
            "issue_key": issue.get("issue_key", str(issue["_id"])[:6].upper()),
            "title": issue.get("title", ""),
            "description": issue.get("description", ""),
            "type": issue.get("type", "task"),
            "priority": issue.get("priority", "medium"),
            "status": issue.get("status", "backlog"),
            "parent_story": parent_story,
            "assignee": self._get_user_details(issue.get("assignee")),
            "created_by": self._get_user_details(issue.get("created_by")),
            "comments": issue.get("comments", []),
            "children": [
                self._format_child_issue(child)
                for child in children
            ],
        }

    def _format_child_issue(self, issue):
        """"
        Format child issue response.
        """
        parent_story = None

        if issue.get("parent_id"):
            parent = self.issue_repository.find_by_id(issue["parent_id"])

            if parent:
                parent_story = {
                    "issue_id": str(parent["_id"]),
                    "issue_key": parent.get("issue_key", ""),
                    "title": parent.get("title", ""),
                }
        return {
            "issue_id": str(issue["_id"]),
            "issue_key": issue.get("issue_key", str(issue["_id"])[:6].upper()),
            "title": issue.get("title", ""),
            "description": issue.get("description", ""),
            "type": issue.get("type", "task"),
            "priority": issue.get("priority", "medium"),
            "status": issue.get("status", "backlog"),
            "parent_story": parent_story,
            "assignee": self._get_user_details(issue.get("assignee")),
            "created_by": self._get_user_details(issue.get("created_by")),
            "comments": issue.get("comments", []),
            "children": [],
        }

    def get_project_issues(
        self,
        project_id: str,
        page: int,
        limit: int,
        status: str | None,
        priority: str | None,
        assignee: str | None,
        search: str | None,
    ):
        """
        Fetch project issues with pagination and filters.
        """
        project_object_id = self._get_project_object_id(project_id)
        project = self.issue_repository.find_project_by_id(project_object_id)

        if not project:
            raise ProjectNotFoundException()

        query = {"project_id": project_object_id}

        if status and status != "all":
            query["status"] = status

        if priority and priority != "all":
            query["priority"] = priority

        if assignee and assignee != "all":
            query["assignee"] = ObjectId(assignee)

        if search:
            parent_ids = self.issue_repository.find_parent_ids_by_child_search(
                project_object_id,
                search,
            )

            query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"issue_key": {"$regex": search, "$options": "i"}},
            {"status": {"$regex": search, "$options": "i"}},
            {"priority": {"$regex": search, "$options": "i"}},
            {"type": {"$regex": search, "$options": "i"}},
            {"_id": {"$in": parent_ids}},
    ]

        total = self.issue_repository.count_parent_issues(query)

        parent_issues = self.issue_repository.get_parent_issues(
            query,
            page,
            limit,
        )

        return {
            "items": [
                self._format_issue(issue)
                for issue in parent_issues
            ],
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": math.ceil(total / limit) if total else 1,
        }


    def update_issue_status(self, issue_id: str, status_data, current_user: dict):
        """
        Update issue status.
        """
        issue_object_id = self._get_object_id(issue_id)
        issue = self.issue_repository.find_by_id(issue_object_id)

        if not issue:
            raise IssueNotFoundException()

        current_user_id = str(current_user["_id"])
        current_user_role = current_user["role"]

        assignee_id = issue.get("assignee")

        if (
            current_user_role != "admin"
            and str(assignee_id) != current_user_id
        ):
            raise AssigneeRequiredException()

        current_status = issue["status"]
        new_status = status_data.status

        allowed_transitions = {
            "backlog": ["todo"],
            "todo": ["in_progress"],
            "in_progress": ["done"],
            "done": [],
        }

        if new_status not in allowed_transitions.get(current_status, []):
            raise InvalidIssueStatusTransitionException()

        self.issue_repository.update_status(
            issue_object_id,
            new_status,
            datetime.now(UTC),
        )

    def _validate_parent_issue(self, parent_id: str | None, project_object_id):
        """
        Validate parent issue.
        """
        if not parent_id:
            return None

        try:
            parent_object_id = ObjectId(parent_id)
        except InvalidId:
            raise InvalidParentIssueException()

        parent_issue = self.issue_repository.find_by_id(parent_object_id)

        if not parent_issue:
            raise InvalidParentIssueException("Parent issue not found")

        if parent_issue["type"] != "story":
            raise InvalidParentIssueException()

        if parent_issue["project_id"] != project_object_id:
            raise InvalidParentIssueException(
                "Parent issue must belong to the same project"
            )

        return parent_id

    def get_project_stories(self, project_id: str):
        """
        Fetch story issues of a project.
        """
        project_object_id = self._get_project_object_id(project_id)
        project = self.issue_repository.find_project_by_id(project_object_id)

        if not project:
            raise ProjectNotFoundException()

        stories = self.issue_repository.get_project_stories(project_object_id)

        return [
            {
                "issue_id": str(story["_id"]),
                "issue_key": story.get("issue_key", ""),
                "title": story.get("title", ""),
            }
            for story in stories
    ]

    def add_comment(self, issue_id, request):
        """
        Add comments to issues.
        """
        issue_object_id = self._get_object_id(issue_id)
        issue = self.issue_repository.find_by_id(issue_object_id)

        if not issue:
            raise IssueNotFoundException()

        comment_user = self.user_repository.find_by_id(request.user_id)

        if not comment_user:
            raise UserNotFoundException()

        now = datetime.now(UTC)

        comment = {
            "comment_id": str(uuid.uuid4()),
            "user": {
                "user_id": str(comment_user["_id"]),
                "name": comment_user["name"],
                "email": comment_user["email"],
                "role": comment_user["role"],
            },
            "comment": request.comment,
            "created_at": now,
            "updated_at": now,
        }

        self.issue_repository.add_comment(
            issue_object_id,
            comment,
        )

    def update_comment(self, issue_id, comment_id, request):
        """
        Update user's own comment.
        """
        issue_object_id = self._get_object_id(issue_id)
        issue = self.issue_repository.find_by_id(issue_object_id)

        if not issue:
            raise IssueNotFoundException()

        comment = next(
            (
                comment for comment in issue.get("comments", [])
                if comment["comment_id"] == comment_id
            ),
            None,
        )

        if not comment:
            raise CommentNotFoundException()

        if comment["user"]["user_id"] != request.user_id:
            raise CommentPermissionDeniedException()

        self.issue_repository.update_comment(
            issue_object_id,
            comment_id,
            request.comment,
        )

    def delete_comment(self, issue_id, comment_id, user_id):
        """
        Delete user's own comment.
        """
        issue_object_id = self._get_object_id(issue_id)
        issue = self.issue_repository.find_by_id(issue_object_id)


        if not issue:
            raise IssueNotFoundException()

        comment = next(
            (
                comment for comment in issue.get("comments", [])
                if comment["comment_id"] == comment_id
            ),
            None,
        )

        if not comment:
            raise CommentNotFoundException()

        if comment["user"]["user_id"] != user_id:
            raise CommentPermissionDeniedException()

        self.issue_repository.delete_comment(
            issue_object_id,
            comment_id,
        )

