from mechanics.technology.tech_upgrade import *
from systems.rng_system import Generator, RngSystem
from utils.singleton import Singleton


UPGRADES = [TripleShot, DoubleShot, NarrowVision, ReinforcedBullets, NumberOne]


class TechUpgradeSystem(metaclass=Singleton):
    def __init__(self):
        self.available_upgrades = UPGRADES
        self.selected_upgrades = set()
        self.random_generator = RngSystem.get_instance().get_rng(Generator.TECHNOLOGY)

    def set_state(self, available_upgrades, selected_upgrades):
        self.available_upgrades = available_upgrades
        self.selected_upgrades = selected_upgrades

    def get_random_upgrade(self):
        # Get random upgrade from available upgrade using self.random_generator
        # Remove the upgrade from available upgrades
        # Add the upgrade to selected upgrades
        if len(self.available_upgrades) == 0:
            return None
        new_upgrade = self.random_generator.choice(self.available_upgrades)
        self.selected_upgrades.add(new_upgrade)
        self.available_upgrades.remove(new_upgrade)
        return new_upgrade
