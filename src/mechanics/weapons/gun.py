from mechanics.weapons.weapon import Weapon


class Gun(Weapon):
    def __init__(self):
        super().__init__(
            damage=10,
            cooldown=0.5,
            bullet_speed=10,
            gun_offset=20,
        )
