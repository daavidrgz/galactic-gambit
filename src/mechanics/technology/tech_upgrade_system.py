from mechanics.technology.tech_upgrade import (
    DoubleShot,
    NarrowVision,
    NumberOne,
    HardBullets,
    TripleShot,
)
from mechanics.upgrade_system import UpgradeSystem
from systems.rng_system import Generator, RngSystem
from utils.singleton import Singleton


TECH_UPGRADES = [TripleShot, DoubleShot, NarrowVision, HardBullets, NumberOne]


class TechUpgradeSystem(UpgradeSystem, metaclass=Singleton):
    def get_available_upgrades(self):
        return TECH_UPGRADES

    def get_random_generator(self):
        return Generator.TECHNOLOGY
