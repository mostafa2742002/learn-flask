import json
from pathlib import Path

from ticket_model import Ticket
from ticket_status import TicketStatus


DATA_FILE = Path("tickets.json")


def ticket_to_dict(ticket):
    return {
        "id": ticket.id,
        "title": ticket.title,
        "status": ticket.status.value,
        "description": ticket.description
    }


def dict_to_ticket(data):
    return Ticket(
        id=data["id"],
        title=data["title"],
        status=TicketStatus(data["status"]),
        description=data["description"]
    )


def load_tickets():
    if not DATA_FILE.exists():
        return [
            Ticket(1, "Login problem", TicketStatus.OPEN, "User cannot login to the system."),
            Ticket(2, "Payment failed", TicketStatus.IN_PROGRESS, "Payment was rejected by the bank."),
            Ticket(3, "Account locked", TicketStatus.RESOLVED, "Account was locked after many failed attempts.")
        ]

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    return [dict_to_ticket(item) for item in data]


tickets = load_tickets()

def save_all():
    with open(DATA_FILE, "w") as file:
        json.dump([ticket_to_dict(ticket) for ticket in tickets], file, indent=4)


def find_all():
    return tickets


def find_by_id(ticket_id):
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket

    return None


def save(ticket):
    tickets.append(ticket)
    save_all()
    return ticket


def delete_by_id(ticket_id):
    ticket = find_by_id(ticket_id)

    if ticket is None:
        return False

    tickets.remove(ticket)
    save_all()
    return True


def get_next_id():
    if len(tickets) == 0:
        return 1

    return max(ticket.id for ticket in tickets) + 1