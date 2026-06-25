from datetime import datetime

def user_model(name: str, email: str, hashed_password: str, role: str = "member"):
    return {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }