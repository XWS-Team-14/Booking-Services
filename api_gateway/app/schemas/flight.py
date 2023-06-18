from pydantic import BaseModel


class TicketPurchase(BaseModel):
    flight_id: str
    num_of_tickets: str
