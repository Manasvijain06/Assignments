from pydantic import BaseModel, Field

class CreateProjectRequest(BaseModel):
    """
    Project Creation Request Schema.
    """

    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    project_key: str = Field(min_length=2, max_length=10)

class UpdateProjectRequest(BaseModel):
    """
    Request schema for updating project details.
    """
    description: str = Field(min_length=3, max_length=100)

class ProjectMemberRequest(BaseModel):
    """
    Request schema for updating project member.
    """
    user_id: str

class AddMemberRequest(BaseModel):
    """
    Request schema for adding a member to a project.
    """
    admin_id: str
    member_id: str


class RemoveMemberRequest(BaseModel):
    """
    Request schema for removing a member from a project.
    """

    admin_id: str
    member_id: str
