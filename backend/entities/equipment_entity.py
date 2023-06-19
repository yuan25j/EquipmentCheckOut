"""Table for all equipment in the database"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from ..models import Equipment

class EquipmentEntity(EntityBase):
    __tablename__ = 'equipment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, default='')
    type: Mapped[str] = mapped_column(String(32), nullable=False, index=True, default='')
    status: Mapped[int] = mapped_column(Integer, index=True)
    notes: Mapped[str] = mapped_column(String(200), nullable=False, default='')

    reservations: Mapped['ReservationEntity'] = relationship(back_populates='equipment', cascade="all, delete")

    @classmethod
    def from_model(cls, model: Equipment) -> Self:
        return cls(
            id=model.id,
            name=model.name,
            type=model.type,
            status=model.status,
            notes=model.notes,
        )
    
    def to_model(self) -> Equipment:
        return Equipment(
            id=self.id,
            name=self.name,
            type=self.type,
            status=self.status,
            notes=self.notes,
        )
    
    def update(self, model: Equipment) -> None:
        self.name = model.name
        self.type = model.type
        self.status = model.status
        self.notes = model.notes