from mechanics.weapons.weapon import Weapon


class Sniper(Weapon):
    def __init__(self):
        super().__init__(
            damage=100,
            cooldown=2000,
            bullet_speed=1,
            gun_offset=50,
        )
