from database import get_connection
from user_model import User


def row_to_user(row):
    return User(
        id=row["id"],
        name=row["name"],
        email=row["email"],
        password=row["password"]
    )


def save(user):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        """,
        (user.name, user.email, user.password)
    )

    connection.commit()

    user.id = cursor.lastrowid

    connection.close()

    return user


def find_by_email(email):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return row_to_user(row)