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


class HardBullets(TechUpgrade):
    name = "Reinforced Bullets"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.bullet_damage *= 1.5
        gun.cooldown *= 1.5


class NumberOne(TechUpgrade):
    name = "Number One"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.bullet_damage *= 0.5
        gun.cooldown *= 0.5


class GlassCannon(TechUpgrade):
    name = "Glass Cannon"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.bullet_damage *= 2
        gun.bullet_lifetime *= 0.5


class Shotgun(TechUpgrade):
    name = "Shotgun"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.n_bullets += 3
        gun.spread = math.pi / 4
        gun.bullet_damage *= 3
        gun.bullet_lifetime *= 0.4
        gun.cooldown *= 1.3


class Sniper(TechUpgrade):
    name = "Sniper"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.bullet_damage *= 4
        gun.bullet_lifetime *= 3
        gun.cooldown *= 3


class BoxPunch(TechUpgrade):
    name = "Box Punch"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.bullet_knockback *= 1.5
        gun.cooldown *= 1.2


class LightWeight(TechUpgrade):
    name = "Light Weight"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        gun.bullet_knockback *= 0.5
        gun.cooldown *= 0.8


class RailwayCannon(TechUpgrade):
    name = "Railway Cannon"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        speed_rate = 1.3
        gun.bullet_speed *= speed_rate
        gun.bullet_lifetime *= 1 / speed_rate
        gun.bullet_damage *= 0.8
        gun.cooldown *= 0.9
        gun.bullet_knockback *= 1.2


class Mace(TechUpgrade):
    name = "Mace"
    icon = Resource.BLACKHOLE_ICON

    def apply(gun):
        speed_rate = 0.5
        gun.bullet_speed *= speed_rate
        gun.bullet_lifetime *= 1 / speed_rate
        gun.bullet_damage *= 1.3
        gun.bullet_knockback *= 1.3
