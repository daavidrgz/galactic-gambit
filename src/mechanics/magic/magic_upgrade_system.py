from mechanics.magic.magic_upgrade import *
from mechanics.upgrade_system import UpgradeSystem
from systems.rng_system import Generator
from utils.singleton import Singleton


MAGIC_UPGRADES = [
    TitansMight,
    SerpentStrike,
    WaveformCannon,
    CrushingStutter,
    PrismaticAura,
    PortableInstability,
    GhostlyShot,
    ViciousAim,
]


class MagicUpgradeSystem(UpgradeSystem, metaclass=Singleton):
    def get_available_upgrades(self):
        return MAGIC_UPGRADES

    def get_random_generator(self):
        return Generator.MAGIC
