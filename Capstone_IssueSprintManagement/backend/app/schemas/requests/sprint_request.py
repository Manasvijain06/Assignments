from datetime import date

from pydantic import BaseModel, Field, model_validator


class CreateSprintRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    project_id: str
    created_by: str
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("Start date cannot be greater than end date")

        return self


class SprintIssueRequest(BaseModel):
    issue_id: str