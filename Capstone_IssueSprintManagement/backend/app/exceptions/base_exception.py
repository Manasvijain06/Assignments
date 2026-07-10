class BaseAppException(Exception):
    """
    Base class for all custom application exceptions.
    """

    default_message = "Application error"

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)