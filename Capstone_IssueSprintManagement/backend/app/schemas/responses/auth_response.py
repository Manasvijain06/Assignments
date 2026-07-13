from pydantic import BaseModel, EmailStr


class UserRegisterResponse(BaseModel):
    """
    User registration response schema.
    """
    message: str
    user_id: str


class UserLoginResponse(BaseModel):
    """
    User login response schema.
    """
    message: str
    user_id: str
    name: str
    email: EmailStr
    role: str
    access_token: str
    token_type: str

class UserListResponse(BaseModel):
    """
    Response schema for user list.
    """
    user_id: str
    name: str
    email: EmailStr
    role: str

class AdminAccessResponse(BaseModel):
    """
    Response returned after successful admin authorization.
    """
    message: str
    user_id: str
    email: EmailStr
    role: str