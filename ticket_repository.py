from database import get_connection
from ticket_model import Ticket
from ticket_status import TicketStatus


def row_to_ticket(row):
    return Ticket(
        id=row["id"],
        title=row["title"],
        status=TicketStatus(row["status"]),
        description=row["description"],
        user_id=row["user_id"],
        created_at=row["created_at"]
    )


def find_all():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM tickets ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return [row_to_ticket(row) for row in rows]


def find_by_id(ticket_id):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return row_to_ticket(row)


def save(ticket):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tickets (title, status, description, user_id, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (ticket.title, ticket.status.value, ticket.description, ticket.user_id, ticket.created_at)
    )

    connection.commit()

    ticket.id = cursor.lastrowid

    connection.close()

    return ticket


def update(ticket):
    connection = get_connection()

    connection.execute(
        """
        UPDATE tickets
        SET title = ?, status = ?, description = ?
        WHERE id = ?
        """,
        (ticket.title, ticket.status.value, ticket.description, ticket.id, ticket.user_id)
    )

    connection.commit()
    connection.close()

    return ticket


def delete_by_id(ticket_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0 # Returns True if a row was deleted, False otherwise


def find_by_status(status):
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM tickets WHERE status = ? ORDER BY id DESC",
        (status,)
    ).fetchall()

    connection.close()

    return [row_to_ticket(row) for row in rows]


def search_by_keyword(keyword):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT * FROM tickets
        WHERE title LIKE ? OR description LIKE ?
        ORDER BY id DESC
        """,
        (f"%{keyword}%", f"%{keyword}%")
    ).fetchall()

    # we use % to allow for partial matches in the search

    connection.close()

    return [row_to_ticket(row) for row in rows]


def find_by_filters(status, keyword,limit=10, offset=0):
    connection = get_connection()

    sql = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if status:
        sql += " AND status = ?"
        params.append(status)

    if keyword:
        sql += " AND (title LIKE ? OR description LIKE ?)"
        params.append(f"%{keyword}%")
        params.append(f"%{keyword}%")

    sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.append(limit)
    params.append(offset)

    rows = connection.execute(sql, params).fetchall()

    connection.close()

    return [row_to_ticket(row) for row in rows]