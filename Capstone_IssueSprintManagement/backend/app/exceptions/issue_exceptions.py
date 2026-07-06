class IssueNotFoundException(Exception):
    def __init__(self, message="Issue not found"):
        self.message = message
        super().__init__(self.message)


class InvalidIssueStatusTransitionException(Exception):
    def __init__(self, message="Invalid issue status transition"):
        self.message = message
        super().__init__(self.message)


class AssigneeRequiredException(Exception):
    def __init__(self, message="Only the assigned user can update issue status"):
        self.message = message
        super().__init__(self.message)

class InvalidParentIssueException(Exception):
    def __init__(self, message="Parent issue must be a story"):
        self.message = message
        super().__init__(self.message)