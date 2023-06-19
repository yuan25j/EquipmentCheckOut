import pytest

from sqlalchemy.orm import Session
from ...models import Equipment, User, Role, Permission
from ...entities import EquipmentEntity, UserEntity, RoleEntity, PermissionEntity
from ...services import EquipmentService, PermissionService, UserPermissionError

# Mock data
monitor1 = Equipment(id=1, name='Asus', type='monitor', status=0, notes='')

monitor2 = Equipment(id=2, name='Dell', type='monitor', status=1, notes='')

keyboard = Equipment(id=3, name='Logitech', type='keyboard', status=0, notes='f key broken')

camera = Equipment(id=4, name='Sony', type='camera', status=1, notes='')

laptop1 = Equipment(id=5, name='Lenovo', type='laptop', status=1, notes='has a short battery life')

laptop2 = Equipment(id=6, name='Lenovo', type='laptop', status=1, notes='')

models = [
    monitor1,
    monitor2,
    keyboard,
    camera,
    laptop1,
    laptop2
]

staff = User(id=1, pid=888888888, onyen='staff',
                  email='staff@unc.edu')
staff_role = Role(id=1, name='staff')
staff_permission: Permission

user = User(id=2, pid=111111111, onyen='user', email='user@unc.edu')

@pytest.fixture(autouse=True)
def setup(test_session: Session):
    # Bootstrap equipment data
    to_entity = EquipmentEntity.from_model
    test_session.add_all([to_entity(model) for model in models])

    # Bootstrap staff and role
    staff_entity = UserEntity.from_model(staff)
    test_session.add(staff_entity)
    staff_role_entity = RoleEntity.from_model(staff_role)
    staff_role_entity.users.append(staff_entity)
    test_session.add(staff_role_entity)
    staff_permission_entity = PermissionEntity(action='equipment.*', resource='equipment/*', role=staff_role_entity)
    test_session.add(staff_permission_entity)

    # Bootstrap user without any permissions
    user_entity = UserEntity.from_model(user)
    test_session.add(user_entity)

    test_session.commit()

    global staff_permission
    staff_permission = staff_permission_entity.to_model()
    yield

# Set up service
@pytest.fixture()
def equipment_service(test_session: Session):
    return EquipmentService(test_session, PermissionService(test_session))

def test_get_by_id1(equipment_service: EquipmentService):
    query_result = equipment_service.get(camera.id)
    assert (camera == query_result) is True

def test_get_by_id2(equipment_service: EquipmentService):
    query_result = equipment_service.get(laptop1.id)
    assert (laptop1 == query_result) is True

def test_filter_type(equipment_service: EquipmentService):
    expected = [laptop1, laptop2]
    query_result = equipment_service.filter_type('laptop')
    assert (expected == query_result) is True

def test_filter_status0(equipment_service: EquipmentService):
    expected = [monitor1, keyboard]
    query_result = equipment_service.filter_status(0)
    assert (expected == query_result) is True

def test_filter_status1(equipment_service: EquipmentService):
    expected = [monitor2, camera, laptop1, laptop2]
    query_result = equipment_service.filter_status(1)
    assert (expected == query_result) is True

def test_list(equipment_service: EquipmentService):
    query_result = equipment_service.list()
    assert (query_result == models) is True

def test_update_success(equipment_service: EquipmentService):
    thing_to_change = keyboard
    thing_to_change.name = 'Razer'
    query_result = equipment_service.update(thing_to_change, staff)
    assert (thing_to_change == query_result) is True

def test_update_failure_equipment_not_exist(equipment_service: EquipmentService):
    thing = Equipment(id=8, name='Sony', type='TV', status=1)
    query_result = equipment_service.update(thing, staff)
    assert (query_result is None) is True

def test_update_failure_invalid_user(equipment_service: EquipmentService):
    thing_to_change = keyboard
    thing_to_change.name = 'Razer'
    try:
        equipment_service.update(thing_to_change, user)
        assert False
    except UserPermissionError:
        assert True
    except Exception as e:
        print('Wrong error in test for updating with invalid user:')
        print(str(e))
        assert False


def test_add(equipment_service: EquipmentService):
    thing = Equipment(id=7, name='Apple', type='laptop', status=1, notes='')
    equipment_service.add(thing, staff)
    assert (equipment_service.get(7) == thing) is True

def test_add_invalid_user(equipment_service: EquipmentService):
    thing = Equipment(id=7, name='Apple', type='laptop', status=1, notes='')
    try:
        equipment_service.add(thing, user)
        assert False
    except UserPermissionError:
        assert True
    except Exception as e:
        print('Wrong error in test for adding with invalid user:')
        print(str(e))
        assert False

def test_remove(equipment_service: EquipmentService):
    equipment_service.remove(monitor1.id, staff)
    assert (equipment_service.get(1) is None) is True

def test_remove_invalid_user(equipment_service: EquipmentService):
    try:
        equipment_service.remove(monitor1.id, user)
        assert False
    except UserPermissionError:
        assert True
    except Exception as e:
        print('Wrong error in test for removing with invalid user:')
        print(str(e))
        assert False

def test_remove_not_exist(equipment_service: EquipmentService):
    thing = Equipment(id=7, name='Apple', type='laptop', status=1, notes='')
    equipment_service.remove(thing.id, staff)
    assert (equipment_service.get(7) is None) is True