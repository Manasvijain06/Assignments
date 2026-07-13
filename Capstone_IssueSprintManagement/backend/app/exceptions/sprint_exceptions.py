class SprintNotFoundException(Exception):
    def __init__(self, message="Sprint not found"):
        self.message = message
        super().__init__(self.message)


class SprintCreationFailedException(Exception):
    def __init__(self, message="Failed to create sprint"):
        self.message = message
        super().__init__(self.message)


class DoneIssueCannotBeAddedException(Exception):
    def __init__(self, message="DONE issues cannot be added to sprint"):
        self.message = message
        super().__init__(self.message)


class IssueAlreadyInSprintException(Exception):
    def __init__(self, message="Issue already added to sprint"):
        self.message = message
        super().__init__(self.message)

class SprintAlreadyExistsException(Exception):
    def __init__(self, message="Sprint name already exists in this project"):
        self.message = message
        super().__init__(self.message)