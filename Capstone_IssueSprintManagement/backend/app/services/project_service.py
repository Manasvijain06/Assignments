from bson import ObjectId
from bson.errors import InvalidId

from app.exceptions.project_exceptions import (
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
)
from app.exceptions.user_exceptions import (
    UserNotFoundException,
    AdminAccessRequiredException,
)
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.models.project_model import ProjectModel


class ProjectService:
    """
    Business logic for project management.
    """

    def __init__(self, db):
        self.project_repository = ProjectRepository(db)
        self.user_repository = UserRepository(db)

    def _get_object_id(self, object_id: str):
        """
        Convert string id to ObjectId.
        """
        try:
            return ObjectId(object_id)
        except InvalidId as exc:
            raise ProjectNotFoundException() from exc

    def _validate_admin(self, admin_id: str):
        """
        Validate Admin role.
        """
        admin = self.user_repository.find_by_id(admin_id)

        if not admin:
            raise UserNotFoundException()

        if admin["role"] != "admin":
            raise AdminAccessRequiredException()

        return admin

    def create_project(self, project_data, admin_id: str):
        """
        Create a new project.
        Only Admin users are allowed.
        """
        self._validate_admin(admin_id)

        existing_project = self.project_repository.find_by_key(
            project_data.project_key)

        if existing_project:
            raise ProjectAlreadyExistsException()

        project = ProjectModel.build(
            name=project_data.name,
            description=project_data.description,
            project_key=project_data.project_key,
            members=[],
            created_by=admin_id
        )

        result = self.project_repository.create_project(project)
        return str(result.inserted_id)

    def get_all_projects(self):
        """
        Fetch a list of all projects.
        """
        projects = self.project_repository.get_all_projects()
        project_list = []

        for project in projects:
            members = []

            for member_id in project.get("members", []):
                user = self.user_repository.find_by_id(str(member_id))

                if user:
                    members.append(
                        {
                        "user_id": str(user["_id"]),
                        "name": user["name"],
                        "email": user["email"],
                        "role": user["role"],
                        }
                    )

            creator = self.user_repository.find_by_id(
                str(project["created_by"])
            )

            project_list.append(
                {
                "project_id": str(project["_id"]),
                "name": project["name"],
                "description": project["description"],
                "project_key": project["project_key"],
                "members": members,
                "created_by": {
                    "user_id": str(creator["_id"]),
                    "name": creator["name"],
                    "email": creator["email"],
                }
                if creator
                else None,
                }
            )

        return project_list

    def update_project(self, project_id: str, project_data):
        """
        Update the project description.
        """
        project_object_id = self._get_object_id(project_id)
        project = self.project_repository.find_by_id(project_object_id)

        if not project:
            raise ProjectNotFoundException()

        self.project_repository.update_description(
            project_object_id,
            project_data.description,
        )

    def delete_project(self, project_id: str):
        """
        Delete a project.
        """
        project_object_id = self._get_object_id(project_id)
        project = self.project_repository.find_by_id(project_object_id)

        if not project:
            raise ProjectNotFoundException()

        self.project_repository.delete_project(project_object_id)

    def add_member(self, project_id: str, admin_id: str, member_id: str):
        """
        Add a member to a project.
        Only Admin users are allowed.
        """
        self._validate_admin(admin_id)

        project_object_id = self._get_object_id(project_id)
        member_object_id = self._get_object_id(member_id)

        project = self.project_repository.find_by_id(project_object_id)

        if not project:
            raise ProjectNotFoundException()

        member = self.user_repository.find_by_id(member_id)

        if not member:
            raise UserNotFoundException()

        if member_object_id in project.get("members", []):
            raise MemberAlreadyAssignedException()

        self.project_repository.add_member(project_object_id, member_object_id)

    def remove_member(self, project_id: str, admin_id: str, member_id: str):
        """
        Remove a member or viewer from a project.
        Only admin users can remove members.
        """
        self._validate_admin(admin_id)

        project_object_id = self._get_object_id(project_id)
        member_object_id = self._get_object_id(member_id)

        project = self.project_repository.find_by_id(project_object_id)

        if not project:
            raise ProjectNotFoundException()

        if member_object_id not in project.get("members", []):
            raise MemberNotAssignedException()

        self.project_repository.remove_member(
            project_object_id,
            member_object_id,
        )
