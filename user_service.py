from werkzeug.security import generate_password_hash, check_password_hash   

from user_model import User
from user_repository import save, find_by_email


def register_user(name, email, password):
    if name.strip() == "":
        return None, "Name is required"

    if email.strip() == "":
        return None, "Email is required"

    if password.strip() == "":
        return None, "Password is required"

    existing_user = find_by_email(email)

    if existing_user is not None:
        return None, "Email already exists"

    hashed_password = generate_password_hash(password)

    user = User(
        id=None,
        name=name,
        email=email,
        password=hashed_password
    )

    saved_user = save(user)

    return saved_user, "Account created successfully"


def login_user(email, password):
    if email.strip() == "":
        return None, "Email is required"

    if password.strip() == "":
        return None, "Password is required"

    user = find_by_email(email)

    if user is None:
        return None, "Invalid email or password"

    password_is_correct = check_password_hash(user.password, password)

    if not password_is_correct:
        return None, "Invalid email or password"

    return user, "Logged in successfully"