from systems.rng_system import RngSystem


class UpgradeSystem:
    def __init__(self):
        self.available_upgrades = self.get_available_upgrades()
        self.selected_upgrades = set()
        self.random_generator = RngSystem.get_instance().get_rng(
            self.get_random_generator()
        )

    def set_state(self, state):
        self.available_upgrades, self.selected_upgrades = state

    def get_state(self):
        return self.available_upgrades, self.selected_upgrades

    def get_random_upgrade(self):
        if len(self.available_upgrades) == 0:
            return None
        new_upgrade = self.random_generator.choice(self.available_upgrades)
        self.selected_upgrades.add(new_upgrade)
        self.available_upgrades.remove(new_upgrade)
        return new_upgrade

    # Template pattern
    def get_available_upgrades(self):
        raise NotImplementedError

    def get_random_generator(self):
        raise NotImplementedError
