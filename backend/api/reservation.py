"""This class holds the API methods that accesses the reservations within the database.

This class holds all nessesary methods to interact with the database such as getting
individual reservations, filtering through the reservations,
etc. deemed as nessesary for front-end, end user functionality. The api route for these methods 
is /api/reservation


Typical usage example from frontend service:
     this.http.get<'returntype'>("/api/reservation/<optional-route>");

"""

from fastapi import APIRouter, Depends
from ..services import ReservationService
from ..models import Reservation, User
from .authentication import registered_user

api = APIRouter(prefix="/api/reservation")

@api.get("/{reservation_id}", response_model=Reservation | None, tags=['Reservation'])
def get(reservation_id: int, reservation_svc: ReservationService = Depends()):
    """API route that returns a Reservation Model by reservation_id as a path parameter.

    Args:
        The reservation ID as a path parameter

    Returns:
        The reservation model or null if no reservation id is found
    """
    return reservation_svc.get(reservation_id)

@api.get("/type/{type}", response_model=list[Reservation], tags=['Reservation'])
def filter_type(type: str, reservation_svc: ReservationService = Depends(), subject: User=Depends(registered_user)):
    """API route that returns list of reservations by type as a path parameter.

    Args:
        The type of reservation as a path parameter
        The user trying to list the reservation by type

    Returns:
        A list reservation models or null no reservations of that type are found
    """
    return reservation_svc.filter_type(type)

@api.get("/user/{user_pid}", response_model=list[Reservation], tags=['Reservation'])
def filter_user(user_pid: int, reservation_svc: ReservationService = Depends()):
    """API route that returns list of reservations by user pid path parameter.

    Args:
        The user pid path parameter

    Returns:
        A list reservation models or null no reservations of that user are found
    """
    return reservation_svc.filter_user(user_pid)


@api.get("", response_model=list[Reservation], tags=['Reservation'])
def list(reservation_svc: ReservationService = Depends()):
    """API route that returns a list of all reservations.

    Args:
        None
        
    Returns:
        A list of all reservations
    """
    return reservation_svc.list()

@api.post("", tags=['Reservation'])
def add(reservation: Reservation, reservation_svc: ReservationService = Depends()):
    """API route to add a reservation with a Reservation model as a request body.

    Args:
        A Reservation
        
    Returns:
        None
    """
    reservation_svc.add(reservation)

@api.delete("", tags=['Reservation'])
def remove(reservation_id: int, reservation_svc: ReservationService = Depends()):
    """API route to remove a reservation with a Reservation model as a request body.

    Args:
        A reservation
        
    Returns:
        None
    """
    reservation_svc.remove(reservation_id)