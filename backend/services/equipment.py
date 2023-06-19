"""This class holds the service methods that interact with the database equipment table."""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Equipment, User
from ..entities import EquipmentEntity
from .permission import PermissionService

class EquipmentService:

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    def get(self, id: int) -> Equipment | None:
        """Function that returns an Equipment based on a given id.
        
        Args:
            An id as an integer
            
        Returns:
            The equipment with the given id or None if it doesn't exist"""
        query = select(EquipmentEntity).where(EquipmentEntity.id == id)
        equipment_entity: EquipmentEntity = self._session.scalar(query)
        if equipment_entity is None:
            return None
        else:
            model = equipment_entity.to_model()
            return model
        
    def filter_type(self, type: str) -> list[Equipment]:
        """Funtion that returns a list of Equipment based on the type of equipment.
        
        Args:
            An equipment type as a string
            
        Returns:
            A list of equipment of the given type or an empty list if no equipment fits the criteria"""
        query = select(EquipmentEntity).where(EquipmentEntity.type.ilike(type))
        entities = self._session.execute(query).scalars()
        return [entity.to_model() for entity in entities]
    
    def filter_status(self, status: int) -> list[Equipment]:
        """Function that returns a list of Equipment based on the status of the equipment.

        Args:
            A status represented by an integer (0: unavailable, 1: available)

        Returns:
            A list of equipment of the given status or an empty list if no equipment fits the criteria"""
        query = select(EquipmentEntity).where(EquipmentEntity.status == status)
        entities = self._session.execute(query).scalars()
        return [entity.to_model() for entity in entities]
    
    def list(self) -> list[Equipment]:
        """Function that returns the full list of equipment.
        
        Returns:
            The list of equipment in the database or an empty list if none exist"""
        query = select(EquipmentEntity)
        entities = self._session.execute(query).scalars()
        return [entity.to_model() for entity in entities]
    
    def update(self, equipment: Equipment, subject: User) -> Equipment | None:
        """Function that updates an equipment in the database.
        
        Args:
            An equipment to update
            The user attempting to update the equipment
            
        Returns:
            The equipment that was updated or None if the equipment wasn't in the database
            
        Throws:
            A UserPermissionError if the user doesn't have permission to edit equipment"""
        self._permission.enforce(subject, 'equipment.update', f'equipment/{equipment.id}')
        entity = self._session.get(EquipmentEntity, equipment.id)
        if (entity):
            entity.update(equipment)
            self._session.commit()
        else:
            self._session.commit()
            return None
        return entity.to_model()
    
    def add(self, equipment: Equipment, subject: User):
        """Function that adds an equipment to the database.
        
        Args:
            An equipment to add
            The user attempting to add the equipment
            
        Throws:
            A UserPermissionError if the user doesn't have permission to add equipment"""
        self._permission.enforce(subject, 'equipment.add', 'equipment/*')
        entity = EquipmentEntity.from_model(equipment)
        self._session.add(entity)
        self._session.commit()

    def remove(self, equipment_id: int, subject: User):
        """Function that removes an equipment from the database.
        
        Args:
            The id of the equipment to remove
            The user attempting to remove the equipment
            
        Throws:
            A UserPermissionError if the user doesn't have permission to remove equipment"""
        self._permission.enforce(subject, 'equipment.remove', f'equipment/{equipment_id}')
        entity = self._session.get(EquipmentEntity, equipment_id)
        if (entity):
            self._session.delete(entity)
        self._session.commit()

    def checkout(self, equipment: Equipment):
        """Helper function that marks an equipment as unavailable.
        
        Args:
            The equipment to checkout"""
        equipment.status = 0
        entity = self._session.get(EquipmentEntity, equipment.id)
        entity.update(equipment)

    def checkin(self, equipment: Equipment):
        """Helper function that marks an equipment as available.
        
        Args:
            The equipment to checkout"""
        equipment.status = 1
        entity = self._session.get(EquipmentEntity, equipment.id)
        entity.update(equipment)