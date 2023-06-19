from ...models import User, Equipment, Reservation

# mock user models
root = User(id=1, pid=999999999, onyen='root', first_name="Super", last_name="User",
             email="root@cs.unc.edu", pronouns="they / them")

sol_student = User(id=2, pid=100000000, onyen='sol', first_name="Sol",
               last_name="Student", email="sol@unc.edu", pronouns="they / them")

arden_ambassador = User(id=3, pid=100000001, onyen='arden', first_name="Arden",
               last_name="Ambassador", email="arden@unc.edu", pronouns="they / them")

merritt_manager = User(id=4, pid=100000002, onyen='merritt', first_name="Merritt",
               last_name="Manager", email="merritt@unc.edu", pronouns="they / them")

# mock equipment models
monitor1 = Equipment(id=1, name='Asus', type='monitor', status=1, notes='')

monitor2 = Equipment(id=2, name='Dell', type='monitor', status=1, notes='')

keyboard = Equipment(id=3, name='Logitech', type='keyboard', status=1, notes='f key broken')

camera = Equipment(id=4, name='Sony', type='camera', status=1, notes='')

laptop1 = Equipment(id=5, name='Lenovo', type='laptop', status=1, notes='has a short battery life')

laptop2 = Equipment(id=6, name='Lenovo', type='laptop', status=1, notes='')


reservation1 = Reservation(id=1, type=monitor2.type, user=root, equipment=monitor2, notes="return asap")
monitor2.status = 0 # equipment is now unavailable

reservation2 = Reservation(id=2, type=camera.type, user=sol_student, equipment=camera, notes="")
camera.status = 0 # equipment is now unavailable

models = [
    reservation1,
    reservation2
]