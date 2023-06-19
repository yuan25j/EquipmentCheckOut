"""This class holds the API methods that accesses the equipment within the database.

This class holds all nessesary methods to interact with the database such as getting
individual equipment, filtering through the equipment,
etc. deemed as nessesary for front-end, end user functionality. The api route for these methods 
is /api/equipment

Typical usage example from frontend service:
     this.http.get<'returntype'>("/api/equipment/<optional-route>");

"""

from fastapi import APIRouter, Depends
from ..services import EquipmentService
from ..models import Equipment, User
from .authentication import registered_user

api = APIRouter(prefix="/api/equipment")

@api.get("/{equipment_id}", response_model=Equipment | None, tags=['Equipment'])
def get(equipment_id: int, equipment_svc: EquipmentService = Depends()):
    """API route that returns an Equipment Model by equipment_id as a path parameter.

    Args:
        The equipment ID as a path parameter

    Returns:
        The equipment model or null if no equipment id is found
    """
    return equipment_svc.get(equipment_id)

@api.get("/type/", response_model=list[Equipment] | None, tags=['Equipment'])
def filter_type(type: str = "", equipment_svc: EquipmentService = Depends()):
    """API route that returns a list of Equipment Models by type as a query parameter, specifically, finds equipment with the exact type.

    Args:
        The equipment type

    Returns:
        A list of equipment models with the same type or null if none are found
    """
    return equipment_svc.filter_type(type)

@api.get("/status/", response_model=list[Equipment] | None, tags=['Equipment'])
def filter_status(status: int = 0, equipment_svc: EquipmentService = Depends()):
    """API route that returns a list of Equipment Models by status as a query parameter.

    Args:
        A status of either 1 or 0, where 1 is available

    Returns:
        A list of equipment models with the same status or null if none are found
    """
    return equipment_svc.filter_status(status)

@api.get("", response_model=list[Equipment] | None, tags=['Equipment'])
def list(equipment_svc: EquipmentService = Depends()):
    """API route that returns a list of all Equipment Models.

    Args:
        None

    Returns:
        A list of all equipment models or null if none are in the database
    """
    return equipment_svc.list()

@api.put("", response_model=Equipment | None, tags=['Equipment'])
def update(equipment: Equipment, equipment_svc: EquipmentService = Depends(), subject: User = Depends(registered_user)):
    """API route that updates a pre-existing Equipment Entity by an Equipment Model as a requeset body.

    Args:
        An equipment model

    Returns:
        Returns a Equipment Model
    """
    return equipment_svc.update(equipment, subject)

@api.post("", tags=["Equipment"])
def add(equipment: Equipment, equipment_svc: EquipmentService = Depends(), subject: User = Depends(registered_user)):
    """API route to add an Equipment Entity by an Equipment Model as a request body. 

    Args:
        An equipment model

    Returns:
        None
    """
    equipment_svc.add(equipment, subject)

@api.delete("", tags=["Equipment"])
def remove(equipment_id: int, equipment_svc: EquipmentService = Depends(), subject: User = Depends(registered_user)):
    """API route to remove an Equipment Entity using an equipment id as a query parameter. 

    Args:
        An equipment id as an integer

    Returns:
        None
    """
    equipment_svc.remove(equipment_id, subject)

