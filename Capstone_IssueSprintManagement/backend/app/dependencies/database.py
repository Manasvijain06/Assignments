from fastapi import HTTPException

from app.database import mongodb


def get_db():
    """
    Return database connection.
    """
    if mongodb.db is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized",
        )

    return mongodb.db