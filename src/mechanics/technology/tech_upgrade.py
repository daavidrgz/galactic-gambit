import math

from systems.resource_manager import Resource


class TechUpgrade:
    def apply(gun):
        raise NotImplementedError


class TripleShot(TechUpgrade):
    name = "Triple Shot"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.n_bullets += 2
        gun.spread += math.pi / 24


class DoubleShot(TechUpgrade):

    name = "Double Shot"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.n_bullets += 1
        gun.spread += math.pi / 32


class NarrowVision(TechUpgrade):
    name = "Narrow Vision"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.damage *= 0.7
        # gun.spread -= math.pi / 32
        # TODO: This is not commutative with spread upgrades,
        # order does matter. Is this a problem or a feature?
        gun.spread /= 2


class HardBullets(TechUpgrade):
    name = "Hard Bullets"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.damage *= 1.5
        gun.cooldown *= 1.5


class NumberOne(TechUpgrade):
    name = "Number One"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.damage *= 0.5
        gun.cooldown *= 0.5
