from datetime import datetime, UTC

def user_model(name: str, email: str, hashed_password: str, role: str = "member"):
    now = datetime.now(UTC)
    return {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "created_at": now,
        "updated_at": now
    }