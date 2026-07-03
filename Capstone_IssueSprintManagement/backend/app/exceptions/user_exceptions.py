class UserAlreadyExistsException(Exception):
    def __init__(self, message="Email already registered"):
        self.message = message
        super().__init__(self.message)


class InvalidPasswordEncodingException(Exception):
    def __init__(self, message="Invalid password encoding"):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsException(Exception):
    def __init__(self, message="Invalid email or password"):
        self.message = message
        super().__init__(self.message)