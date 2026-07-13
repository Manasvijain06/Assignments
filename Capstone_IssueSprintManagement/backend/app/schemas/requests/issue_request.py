from typing import Literal
from pydantic import BaseModel, Field


class CreateIssueRequest(BaseModel):
    """
    Request schema for creating an issue.
    """

    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=500)
    type: Literal["task", "bug", "story"]
    priority: Literal["low", "medium", "high"]
    assignee: str
    created_by: str
    parent_id: str | None = None

class UpdateIssueStatusRequest(BaseModel):
    status: Literal[
        "backlog",
        "todo",
        "in_progress",
        "done"
    ]
    updated_by: str