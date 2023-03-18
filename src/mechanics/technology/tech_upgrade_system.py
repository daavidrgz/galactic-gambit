from mechanics.technology.tech_upgrade import (
    BoxPunch,
    DoubleShot,
    Mace,
    NumberOne,
    HardBullets,
    RailwayCannon,
    TripleShot,
    GlassCannon,
    Shotgun,
    Sniper,
)
from mechanics.upgrade_system import UpgradeSystem
from systems.rng_system import Generator
from utils.singleton import Singleton


TECH_UPGRADES = [
    TripleShot,
    DoubleShot,
    HardBullets,
    NumberOne,
    GlassCannon,
    Shotgun,
    Sniper,
    BoxPunch,
    RailwayCannon,
    Mace,
]


class TechUpgradeSystem(UpgradeSystem, metaclass=Singleton):
    def get_available_upgrades(self):
        return TECH_UPGRADES

    def get_random_generator(self):
        return Generator.TECHNOLOGY
