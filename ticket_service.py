from ticket_model import Ticket
from ticket_repository import find_all, find_by_id, save, get_next_id


def get_all_tickets():
    return find_all()


def get_ticket_by_id(ticket_id):
    return find_by_id(ticket_id)


def add_ticket(title, description):
    new_ticket = Ticket(
        id=get_next_id(),
        title=title,
        status="OPEN",
        description=description
    )

    return save(new_ticket)

def resolve_ticket(ticket_id):
    ticket = find_by_id(ticket_id)

    if ticket is None:
        return None

    ticket.status = "RESOLVED"

    return ticket