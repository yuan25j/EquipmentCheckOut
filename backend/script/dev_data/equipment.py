"""Sample Equipment models to use in development"""

from ...models import Equipment

# Names can be more exact in actual use (I'm lazy)
# Status 0 means unavailable and 1 means available (can make enum later if needed)
monitor1 = Equipment(id=1, name='Asus', type='monitor', status=1, notes='')

monitor2 = Equipment(id=2, name='Dell', type='monitor', status=0, notes='')

keyboard = Equipment(id=3, name='Logitech', type='keyboard', status=1, notes='f key broken')

camera = Equipment(id=4, name='Sony', type='camera', status=0, notes='')

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