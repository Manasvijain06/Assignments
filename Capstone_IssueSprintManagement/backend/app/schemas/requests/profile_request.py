from pydantic import BaseModel, Field


class UpdateProfileRequest(BaseModel):
    """
    Request schema for updating user profile.
    """
    name: str = Field(..., min_length=2, max_length=50)


class ChangePasswordRequest(BaseModel):
    """
    Request schema for changing password
    """
    current_password: str
    new_password: str = Field(..., min_length=6)