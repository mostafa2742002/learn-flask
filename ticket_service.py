from ticket_model import Ticket
from ticket_repository import delete_by_id, find_all, find_by_id, save, get_next_id, save_all
from ticket_status import TicketStatus

def get_all_tickets():
    return find_all()


def get_ticket_by_id(ticket_id):
    return find_by_id(ticket_id)


def add_ticket(title, description):
    new_ticket = Ticket(
        id=get_next_id(),
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

    save_all()

    return ticket, "Ticket resolved successfully"

def start_progress_ticket(ticket_id):
    ticket = find_by_id(ticket_id)

    if ticket is None:
        return None, "Ticket not found"

    started = ticket.start_progress()

    if not started:
        return ticket, "Only open tickets can be moved to in progress"

    save_all()

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

    save_all()

    return ticket, "Ticket updated successfully"


def delete_ticket(ticket_id):
    deleted = delete_by_id(ticket_id)

    if not deleted:
        return "Ticket not found"

    return "Ticket deleted successfully"