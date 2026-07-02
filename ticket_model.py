from dataclasses import dataclass
from ticket_status import TicketStatus


@dataclass
class Ticket:
    id: int
    title: str
    status: TicketStatus
    description: str

    def start_progress(self):
        if self.status != TicketStatus.OPEN:
            return False

        self.status = TicketStatus.IN_PROGRESS
        return True

    def resolve(self):
        if self.status != TicketStatus.IN_PROGRESS:
            return False

        self.status = TicketStatus.RESOLVED
        return True