from database import get_connection
from ticket_model import Ticket
from ticket_status import TicketStatus


def row_to_ticket(row):
    return Ticket(
        id=row["id"],
        title=row["title"],
        status=TicketStatus(row["status"]),
        description=row["description"]
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
        INSERT INTO tickets (title, status, description)
        VALUES (?, ?, ?)
        """,
        (ticket.title, ticket.status.value, ticket.description)
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
        (ticket.title, ticket.status.value, ticket.description, ticket.id)
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