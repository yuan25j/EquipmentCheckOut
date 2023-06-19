"""Table for all reservations in the database"""

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from .user_entity import UserEntity
from .equipment_entity import EquipmentEntity
from ..models import Reservation


class ReservationEntity(EntityBase):
    __tablename__ = 'reservation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(32), index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped[UserEntity] = relationship(back_populates="reservations")

    equipment_id: Mapped[int] = mapped_column(ForeignKey('equipment.id'))
    equipment: Mapped[EquipmentEntity] = relationship(back_populates="reservations")
    
    notes: Mapped[str] = mapped_column(String(200), nullable=True)

    @classmethod
    def from_model(cls, model: Reservation) -> Self:
        return cls(
            id=model.id,
            type=model.type,
            user_id=model.user.id,
            equipment_id=model.equipment.id,
            notes=model.notes,
        )
    
    def to_model(self) -> Reservation:
        return Reservation(
            id=self.id,
            type=self.type,
            user = self.user.to_model(),
            equipment = self.equipment.to_model(),
            notes = self.notes
        )