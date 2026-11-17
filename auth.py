from storage import load_records, append_record


def authenticate_user(username, password):
    username = username.strip()
    password = password.strip()
    rows = load_records("users.txt")

    for row in rows:
        if len(row) < 3:
            continue
        stored_user, stored_pass, role = row[0], row[1], row[2]
        if stored_user == username and stored_pass == password:
            return {"username": stored_user, "role": role}

    return None


def is_admin(user):
    return bool(user and user.get("role") == "admin")


def create_user(username, password, role="instructor"):
    username = username.strip()
    password = password.strip()
    role = role.strip().lower()

    if not username or not password:
        raise ValueError("Username and password are required.")
    if role not in ("admin", "instructor"):
        raise ValueError("Role must be 'admin' or 'instructor'.")

    rows = load_records("users.txt")
    for row in rows:
        if row and row[0] == username:
            raise ValueError(f"User '{username}' already exists.")

    append_record("users.txt", [username, password, role])
    return {"username": username, "role": role}


def load_users() -> list[dict[str, str]]:
    users: list[dict[str, str]] = []
    try:
        rows = load_records(USERS_FILE)
    except Exception:
        return users

    for row in rows:
        parts = [part.strip() for part in row.split("|")]
        if len(parts) == 4 and all(parts):
            username, salt, pw_hash, role = parts
            users.append(
                {
                    "username": username,
                    "salt": salt,
                    "hash": pw_hash,
                    "role": role,
                }
            )
    return users