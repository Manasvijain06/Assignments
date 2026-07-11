from fastapi import Depends, HTTPException, status

from app.dependencies.authentication import get_current_user


class RoleChecker:
    """
    Check whether the current user has an allowed role.
    """

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        current_user: dict = Depends(get_current_user),
    ):
        if current_user["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to perform this action.",
            )

        return current_user