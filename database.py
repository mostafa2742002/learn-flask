import sqlite3


DATABASE_NAME = "tickets.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row # this allows us to access columns by name instead of index
    return connection


def init_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    columns = connection.execute("PRAGMA table_info(tickets)").fetchall()
    column_names = [column["name"] for column in columns]

    if "user_id" not in column_names:
        connection.execute("ALTER TABLE tickets ADD COLUMN user_id INTEGER")

    if "created_at" not in column_names:
        connection.execute("ALTER TABLE tickets ADD COLUMN created_at TEXT")



    connection.commit()
    connection.close()