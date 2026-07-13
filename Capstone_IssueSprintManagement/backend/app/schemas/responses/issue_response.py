from pydantic import BaseModel


class CreateIssueResponse(BaseModel):
    """
    Response returned after creating an issue.
    """

    message: str
    issue_id: str