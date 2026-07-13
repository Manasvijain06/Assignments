from app.exceptions.base_exception import BaseAppException

class UserAlreadyExistsException(BaseAppException):
    default_message = "Email already registered"


class InvalidPasswordEncodingException(BaseAppException):
    default_message = "Invalid password encoding"


class InvalidCredentialsException(BaseAppException):
    default_message = "Invalid email or password"


class UserNotFoundException(BaseAppException):
    default_message = "User not found"


class AdminAccessRequiredException(BaseAppException):
    default_message = "Admin access required"

class SamePasswordException(BaseAppException):
    default_message = "New password must be different from current password"