from datetime import datetime, UTC


def project_model(name, description, project_key, members, created_by):
    now = datetime.now(UTC)

    return {
        "name": name,
        "description": description,
        "project_key": project_key,
        "members": members,
        "created_by": created_by,
        "created_at": now,
        "updated_at": now
    }