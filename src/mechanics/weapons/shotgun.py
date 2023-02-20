import math

import numpy as np
from mechanics.weapons.spread_weapon import SpreadWeapon
from mechanics.weapons.weapon import Weapon


class ShotGun(SpreadWeapon):
    def __init__(self):
        super().__init__(
            damage=50,
            cooldown=500,
            bullet_speed=0.7,
            gun_offset=30,
            spread=math.pi / 6,
            n_bullets=3,
        )
