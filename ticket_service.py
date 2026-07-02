from ticket_model import Ticket
from ticket_repository import find_all, find_by_id, find_by_status, save, update, delete_by_id
from ticket_status import TicketStatus

def get_all_tickets():
    return find_all()


def get_ticket_by_id(ticket_id):
    return find_by_id(ticket_id)


def add_ticket(title, description):
    new_ticket = Ticket(
        id=None,
        title=title,
        status=TicketStatus.OPEN,
        description=description
    )

    return save(new_ticket)

def resolve_ticket(ticket_id):
    ticket = find_by_id(ticket_id)

    if ticket is None:
        return None, "Ticket not found"

    resolved = ticket.resolve()

    if not resolved:
        return ticket, "Only in-progress tickets can be resolved"

    update(ticket)

    return ticket, "Ticket resolved successfully"

def start_progress_ticket(ticket_id):
    ticket = find_by_id(ticket_id)

    if ticket is None:
        return None, "Ticket not found"

    started = ticket.start_progress()

    if not started:
        return ticket, "Only open tickets can be moved to in progress"

    update(ticket)

    return ticket, "Ticket moved to in progress"


def update_ticket(ticket_id, title, description):
    ticket = find_by_id(ticket_id)

    if ticket is None:
        return None, "Ticket not found"

    if title.strip() == "":
        return ticket, "Title is required"

    if description.strip() == "":
        return ticket, "Description is required"

    ticket.title = title
    ticket.description = description

    update(ticket)

    return ticket, "Ticket updated successfully"


def delete_ticket(ticket_id):
    deleted = delete_by_id(ticket_id)

    if not deleted:
        return "Ticket not found"

    return "Ticket deleted successfully"


def get_tickets_by_status(status):
    if status is None or status.strip() == "":
        return find_all()

    return find_by_status(status)