from pydantic import BaseModel, Field


class CreateIssueRequest(BaseModel):
    """
    Request schema for creating an issue.
    """

    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=500)
    created_by: str = Field(..., min_length=1)