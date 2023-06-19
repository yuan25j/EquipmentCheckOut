"""Data object to represent equipment that can be checked out."""

from pydantic import BaseModel

class Equipment(BaseModel):
    id: int | None
    name: str
    type: str
    status: int
    notes: str = ''