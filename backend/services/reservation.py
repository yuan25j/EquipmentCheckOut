"""This class holds the service methods that interact with the database reservation table."""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Reservation, User
from ..entities import ReservationEntity, UserEntity
from . import EquipmentService
from .permission import PermissionService



class ReservationService:

    _session: Session
    _equipment_svc: EquipmentService
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), equipment_svc: EquipmentService = Depends(), permission: PermissionService = Depends()):
        self._session = session
        self._equipment_svc = equipment_svc
        self._permission = permission

    def get(self, id: int) -> Reservation | None:
        """Function that returns a reservation based on a given id.
        
        Args:
            An id as an integer
            
        Returns:
            The reservation with the given id or None if it doesn't exist"""
        query = select(ReservationEntity).where(ReservationEntity.id == id)
        reservation_entity: ReservationEntity = self._session.scalar(query)
        if reservation_entity:
            reservationModel = reservation_entity.to_model()
            return reservationModel
        else:
            return None
        
    def filter_type(self, type: str, subject: User) -> list[Reservation]:
        """Funtion that returns a list of reservation based on the type of equipment.
        
        Args:
            An equipment type as a string
            The user attempting to list the reservation by type
            
        Returns:
            A list of reservations of the given type or an empty list if no reservation fits the criteria"""
        self._permission.enforce(subject, 'reservation.filter_type', f'reservation/{type}')
        query = select(ReservationEntity).where(ReservationEntity.type.ilike(type))
        reservationEntities = self._session.execute(query).scalars()
        return [reservationEntity.to_model() for reservationEntity in reservationEntities]
    
    def filter_user(self, user_pid: int) -> list[Reservation]:
        """Funtion that returns a list of reservation based on the user associated with the reservation.
        
        Args:
            A user pid as string
            
        Returns:
            A list of reservations of the given user pid or an empty list if no reservation fits the criteria"""
        userQuery = select(UserEntity).where(UserEntity.pid.__eq__(user_pid))
        userModel = self._session.execute(userQuery).scalar().to_model()
        query = select(ReservationEntity).where(ReservationEntity.user_id.__eq__(userModel.id))
        reservationEntities = self._session.execute(query).scalars()
        return [reservationEntity.to_model() for reservationEntity in reservationEntities]
    
    def list(self) -> list[Reservation]:
        """Funtion that returns all reservations.
        
        Args:
            None
            
        Returns:
            A list of all reservations."""

        query = select(ReservationEntity)
        reservationEntities = self._session.execute(query).scalars()
        return [reservationEntity.to_model() for reservationEntity in reservationEntities]
    
    def add(self, reservation: Reservation):
        """Funtion that adds a reservation to the database table.
        
        Args:
            A reservation object
            
        Returns:
            None"""
        self._equipment_svc.checkout(reservation.equipment)
        reservationEntity = ReservationEntity.from_model(reservation)
        self._session.add(reservationEntity)
        self._session.commit()

    def remove(self, reservation_id: int):
        """Funtion that deletes a reservation to the database table.
        
        Args:
            A reservation id
            
        Returns:
            None"""
        reservationEntity = self._session.get(ReservationEntity, reservation_id)
        if (reservationEntity):
            self._session.delete(reservationEntity)
            reservation = reservationEntity.to_model()
            self._equipment_svc.checkin(reservation.equipment)
        self._session.commit()



