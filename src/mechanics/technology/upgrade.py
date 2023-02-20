import math


class Upgrade:
    def modify_gun(gun):
        pass


class TripleShot(Upgrade):
    def modify_gun(gun):
        gun.n_bullets += 2
        gun.spread += math.pi / 24


class DoubleShot(Upgrade):
    def modify_gun(gun):
        gun.n_bullets += 1
        gun.spread += math.pi / 32


class NarrowVision(Upgrade):
    def modify_gun(gun):
        gun.damage *= 0.7
        gun.spread -= math.pi / 32


class ReinforcedBullets(Upgrade):
    def modify_gun(gun):
        gun.damage *= 1.5
        gun.cooldown *= 1.5


class NumberOne(Upgrade):
    def modify_gun(gun):
        gun.damage *= 0.5
        gun.cooldown *= 0.5
