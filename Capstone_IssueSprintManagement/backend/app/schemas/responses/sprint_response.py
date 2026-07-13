from typing import List
from pydantic import BaseModel


class CreateSprintResponse(BaseModel):
    message: str
    sprint_id: str


class SprintIssueResponse(BaseModel):
    issue_id: str
    issue_key: str
    title: str
    status: str
    type: str


class SprintDetailResponse(BaseModel):
    sprint_id: str
    name: str
    project_id: str
    status: str
    start_date: str
    end_date: str
    total_issues: int
    completed_issues: int
    progress: int
    issues: List[SprintIssueResponse]


class SprintListResponse(BaseModel):
    items: List[SprintDetailResponse]
    total: int
    page: int
    limit: int
    total_pages: int

class SprintStatusResponse(BaseModel):
    message: str