from bson import ObjectId

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
from app.models.project_model import project_model


class ProjectService:

    def __init__(self, db):
        self.projects_collection = db["projects"]
        self.users_collection = db["users"]

    def _validate_admin(self, admin_email: str):
        """
        Validate that the user exists and has the Admin role.
        """
        user = self.users_collection.find_one({"email": admin_email})

        if not user:
            raise UserNotFoundException()

        if user["role"] != "admin":
            raise AdminAccessRequiredException()

        return user

    def create_project(self, project_data, admin_email: str):
        """
        Create a new project.
        Only Admin users are allowed.
        """
        admin_user = self._validate_admin(admin_email)

        existing_project = self.projects_collection.find_one(
            {"project_key": project_data.project_key}
        )

        if existing_project:
            raise ProjectAlreadyExistsException()

        project = project_model(
            name=project_data.name,
            description=project_data.description,
            project_key=project_data.project_key,
            members=project_data.members,
            created_by=admin_user["email"]
        )

        result = self.projects_collection.insert_one(project)
        return str(result.inserted_id)

    def add_member(self, project_id: str, admin_email: str, member_email: str):
        """
        Add a member to a project.
        Only Admin users are allowed.
        """
        self._validate_admin(admin_email)

        project = self.projects_collection.find_one({"_id": ObjectId(project_id)})

        if not project:
            raise ProjectNotFoundException()

        if member_email in project.get("members", []):
            raise MemberAlreadyAssignedException()

        self.projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$addToSet": {"members": member_email}}
        )

    def remove_member(self, project_id: str, admin_email: str, member_email: str):
        """
        Delete a member to a project.
        Only Admin users are allowed.
        """
        self._validate_admin(admin_email)

        project = self.projects_collection.find_one({"_id": ObjectId(project_id)})

        if not project:
            raise ProjectNotFoundException()

        if member_email not in project.get("members", []):
            raise MemberNotAssignedException()

        self.projects_collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$pull": {"members": member_email}}
        )

    def get_all_projects(self):
        """
        Fetch a list of all projects.
        """
        projects = self.projects_collection.find()

        return [
        {
            "project_id": str(project["_id"]),
            "name": project["name"],
            "description": project["description"],
            "project_key": project["project_key"],
            "members": project.get("members", []),
            "created_by": project["created_by"],
        }
        for project in projects
    ]


    def update_project(self, project_id: str, project_data):
        """
        Update the project
        """
        try:
            object_id = ObjectId(project_id)
        except Exception:
            raise ProjectNotFoundException()

        project = self.projects_collection.find_one({"_id": object_id})

        if not project:
            raise ProjectNotFoundException()

        self.projects_collection.update_one(
            {"_id": object_id},
            {
                "$set": {
                "name": project_data.name,
                "description": project_data.description,
                "project_key": project_data.project_key,
                }
            },
        )