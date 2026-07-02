from dataclasses import dataclass
from ticket_status import TicketStatus

@dataclass
class Ticket:
    id: int
    title: str
    status: TicketStatus
    description: str

    def resolve(self):
        self.status = TicketStatus.RESOLVED