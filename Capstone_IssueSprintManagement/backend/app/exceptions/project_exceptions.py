class ProjectAlreadyExistsException(Exception):
    def __init__(self, message="Project key already exists"):
        self.message = message
        super().__init__(self.message)


class ProjectNotFoundException(Exception):
    def __init__(self, message="Project not found"):
        self.message = message
        super().__init__(self.message)


class MemberAlreadyAssignedException(Exception):
    def __init__(self, message="Member already assigned to project"):
        self.message = message
        super().__init__(self.message)


class MemberNotAssignedException(Exception):
    def __init__(self, message="Member is not assigned to project"):
        self.message = message
        super().__init__(self.message)