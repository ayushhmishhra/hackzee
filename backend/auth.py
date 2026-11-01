import re
import bcrypt

from database import get_connection


def validate_password(password):
    """Check whether the password meets security requirements."""

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[^A-Za-z0-9]", password):
        return False, "Password must contain at least one special character."

    return True, "Password is valid."


def signup_user(name, email, password):
    """Register a new user."""

    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "All fields are required."

    valid, message = validate_password(password)

    if not valid:
        return False, message

    # Hash the password before saving it.
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (name, email, password_hash)
            )

        return True, "Account created successfully!"

    except Exception as error:
        if "UNIQUE constraint failed" in str(error):
            return False, "An account with this email already exists."

        return False, "Could not create your account. Please try again."


def login_user(email, password):
    """Authenticate an existing user."""

    email = email.strip().lower()

    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT id, name, email, password_hash
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

    if user is None:
        return False, "Invalid email or password.", None

    password_matches = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    )

    if not password_matches:
        return False, "Invalid email or password.", None

    user_data = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }

    return True, "Login successful!", user_data
