"""Data object to represent reservations from users checking out or returning equipment."""

from pydantic import BaseModel
from . import User, Equipment

class Reservation(BaseModel):
    id: int | None
    type: str
    user: User
    equipment: Equipment
    notes: str | None = None