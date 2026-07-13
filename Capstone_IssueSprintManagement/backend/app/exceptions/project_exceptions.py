from app.exceptions.base_exception import BaseAppException


class ProjectAlreadyExistsException(BaseAppException):
    default_message = "Project key already exists"


class ProjectNotFoundException(BaseAppException):
    default_message = "Project not found"


class MemberAlreadyAssignedException(BaseAppException):
    default_message = "Member already assigned to project"


class MemberNotAssignedException(BaseAppException):
    default_message = "Member is not assigned to project"