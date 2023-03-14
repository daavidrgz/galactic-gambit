from systems.rng_system import RngSystem


class UpgradeSystem:
    def __init__(self):
        self.available_upgrades = self.get_available_upgrades()
        self.num_upgrades = len(self.available_upgrades)
        self.selected_upgrades = set()
        self.random_generator = RngSystem.get_instance().get_rng(
            self.get_random_generator()
        )

    def set_state(self, state):
        self.available_upgrades, self.selected_upgrades = state

    def get_state(self):
        return self.available_upgrades, self.selected_upgrades

    def get_random_upgrades(self, n):
        upgrades_to_pick = min(n, len(self.available_upgrades))
        new_upgrades = self.random_generator.sample(
            self.available_upgrades, upgrades_to_pick
        )
        return new_upgrades

    def pick_upgrade(self, upgrade):
        if upgrade in self.available_upgrades:
            self.selected_upgrades.add(upgrade)
            self.available_upgrades.remove(upgrade)
            return True
        return False

    def get_num_upgrades(self):
        return self.num_upgrades

    # Template pattern
    def get_available_upgrades(self):
        raise NotImplementedError

    def get_random_generator(self):
        raise NotImplementedError
