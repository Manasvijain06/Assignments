from app.exceptions.base_exception import BaseAppException


class SprintNotFoundException(BaseAppException):
    default_message = "Sprint not found"


class SprintCreationFailedException(BaseAppException):
    default_message = "Failed to create sprint"


class DoneIssueCannotBeAddedException(BaseAppException):
    default_message = "DONE issues cannot be added to sprint"


class IssueAlreadyInSprintException(BaseAppException):
    default_message = "Issue already added to sprint"


class SprintAlreadyExistsException(BaseAppException):
    default_message = "Sprint name already exists in this project"


class InvalidSprintStatusException(BaseAppException):
    default_message = "Invalid sprint status transition"