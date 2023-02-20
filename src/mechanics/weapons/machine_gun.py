from mechanics.weapons.weapon import Weapon


class MachineGun(Weapon):
    def __init__(self):
        super().__init__(
            damage=10,
            cooldown=100,
            bullet_speed=1,
            gun_offset=30,
        )
