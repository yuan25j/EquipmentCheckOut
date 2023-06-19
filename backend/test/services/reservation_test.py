import pytest

from sqlalchemy.orm import Session
from ...models import Equipment, Reservation, User, Role, Permission
from ...entities import ReservationEntity, EquipmentEntity, UserEntity, PermissionEntity, RoleEntity
from ...services import ReservationService, EquipmentService, PermissionService, UserPermissionError


# mock data

monitor1 = Equipment(id=1, name='Asus', type='monitor', status=1, notes='')
monitor2 = Equipment(id=2, name='Dell', type='monitor', status=1, notes='')
keyboard = Equipment(id=3, name='Logitech', type='keyboard', status=1, notes='f key broken')
camera = Equipment(id=4, name='Sony', type='camera', status=1, notes='')
laptop1 = Equipment(id=5, name='Lenovo', type='laptop', status=1, notes='has a short battery life')
laptop2 = Equipment(id=6, name='Lenovo', type='laptop', status=1, notes='')

equipmentModels = [
    monitor1,
    monitor2,
    keyboard,
    camera,
    laptop1,
    laptop2
]

root = User(id=1, pid=999999999, onyen='root', first_name="Super", last_name="User",
             email="root@cs.unc.edu", pronouns="they / them")
sol_student = User(id=2, pid=100000000, onyen='sol', first_name="Sol",
               last_name="Student", email="sol@unc.edu", pronouns="they / them")
arden_ambassador = User(id=3, pid=100000001, onyen='arden', first_name="Arden",
               last_name="Ambassador", email="arden@unc.edu", pronouns="they / them")
merritt_manager = User(id=4, pid=100000002, onyen='merritt', first_name="Merritt",
               last_name="Manager", email="merritt@unc.edu", pronouns="they / them")

staff = User(id=5, pid=888888888, onyen='staff',
                  email='staff@unc.edu')
staff_role = Role(id=1, name='staff')
staff_permission: Permission

user = User(id=6, pid=111111111, onyen='user', email='user@unc.edu')

userModels = [
    root,
    sol_student,
    arden_ambassador,
    merritt_manager
]

reservation1 = Reservation(id=1, type=monitor1.type, user=root, equipment=monitor1, notes="")
reservation2 = Reservation(id=2, type=keyboard.type, user=sol_student, equipment=keyboard, notes="")

reservationModels = [
    reservation1,
    reservation2
]



@pytest.fixture(autouse=True)
def setup(test_session: Session):
    # Bootstrap all data
    to_reservation_entity = ReservationEntity.from_model
    to_equipment_entity = EquipmentEntity.from_model
    to_user_entity = UserEntity.from_model

    staff_entity = UserEntity.from_model(staff)
    test_session.add(staff_entity)
    staff_role_entity = RoleEntity.from_model(staff_role)
    staff_role_entity.users.append(staff_entity)
    test_session.add(staff_role_entity)
    staff_permission_entity = PermissionEntity(action='reservation.*', resource='reservation/*', role=staff_role_entity)
    test_session.add(staff_permission_entity)

    
    test_session.add_all([to_reservation_entity(reservationModel) for reservationModel in reservationModels])
    test_session.add_all([to_equipment_entity(equipmentModel) for equipmentModel in equipmentModels])
    test_session.add_all([to_user_entity(userModel) for userModel in userModels])
    test_session.commit()

@pytest.fixture(autouse=True)
def reservation_service(test_session: Session):
    return ReservationService(test_session, EquipmentService(test_session, PermissionService(test_session)), PermissionService(test_session))


def test_get_by_id1(reservation_service: ReservationService):
    query_result = reservation_service.get(reservation1.id)
    assert (reservation1 == query_result) is True

def test_get_by_id2(reservation_service: ReservationService):
    query_result = reservation_service.get(9999)
    assert (None == query_result) is True

def test_filter_type_valid_user(reservation_service: ReservationService):
    query_result = reservation_service.filter_type(reservation1.type, staff)
    assert ([reservation1] == query_result)

def test_filter_type_invalid_user(reservation_service: ReservationService):
    try:
        reservation_service.filter_type(type, user)
        assert False
    except UserPermissionError:
        assert True
    except Exception as e:
        print('Wrong error in test for filter_type with invalid user:')
        print(str(e))
        assert False

def test_filter_user(reservation_service: ReservationService):
    query_result = reservation_service.filter_user(reservation1.user.pid)
    assert ([reservation1] == query_result)

def test_list_valid_user(reservation_service: ReservationService):
    query_result = reservation_service.list()
    assert (reservationModels == query_result) is True

# def test_list_invalid_user(reservation_service: ReservationService):
#     try:
#         reservation_service.list(user)
#         assert False
#     except UserPermissionError:
#         assert True
#     except Exception as e:
#         print('Wrong error in test for list with invalid user:')
#         print(str(e))
#         assert False

def test_add(reservation_service: ReservationService):
    newReservation = Reservation(id=3, type=camera.type, user=merritt_manager, equipment=camera)
    reservation_service.add(newReservation)
    query_result = reservation_service.get(newReservation.id)
    assert (newReservation == query_result) is True

def test_remove(reservation_service: ReservationService):
    reservation_service.remove(reservation2.id)
    query_result = reservation_service.list()
    assert ([reservation1] == query_result) is True




