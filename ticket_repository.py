from ticket_model import Ticket

tickets = [
    Ticket(
        id=1,
        title="Login problem",
        status="OPEN",
        description="User cannot login to the system."
    ),
    Ticket(
        id=2,
        title="Payment failed",
        status="IN_PROGRESS",
        description="Payment was rejected by the bank."
    ),
    Ticket(
        id=3,
        title="Account locked",
        status="RESOLVED",
        description="Account was locked after many failed attempts."
    )
]


def find_all():
    return tickets


def find_by_id(ticket_id):
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket

    return None


def save(ticket):
    tickets.append(ticket)
    return ticket


def get_next_id():
    return len(tickets) + 1