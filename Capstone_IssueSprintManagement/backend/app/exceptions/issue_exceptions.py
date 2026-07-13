from app.exceptions.base_exception import BaseAppException


class IssueNotFoundException(BaseAppException):
    default_message = "Issue not found"


class InvalidIssueStatusTransitionException(BaseAppException):
    default_message = "Invalid issue status transition"


class AssigneeRequiredException(BaseAppException):
    default_message = "Only the assigned user can update issue status"


class InvalidParentIssueException(BaseAppException):
    default_message = "Parent issue must be a story"

class CommentNotFoundException(BaseAppException):
    default_message = "Comment not found"


class CommentPermissionDeniedException(BaseAppException):
    default_message = "You can update or delete only your own comments"