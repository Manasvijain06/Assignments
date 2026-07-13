from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.database import mongodb
from app.utils.jwt_handler import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    """
    Validate JWT token and return the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )

    try:
        payload = decode_access_token(token)
    except JWTError as exc:
        raise credentials_exception from exc

    user_id = payload.get("sub")

    if not user_id:
        raise credentials_exception

    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized.",
        )

    user = mongodb.db["users"].find_one(
        {"_id": __import__("bson").ObjectId(user_id)}
    )

    if not user:
        raise credentials_exception

    return user