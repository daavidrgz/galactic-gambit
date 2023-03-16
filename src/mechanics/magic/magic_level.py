from mechanics.magic.magic_upgrade_system import MagicUpgradeSystem
from utils.observable import Observable


class MagicLevel(Observable):
    __BASE_TARGET_EXP = 20
    __LEVEL_STEP_EXP = 50

    def __init__(
        self,
        initial_level=0,
        initial_exp=0,
    ):
        super().__init__()
        self.level = initial_level
        self.experience = initial_exp
        self.max_level = MagicUpgradeSystem().get_num_upgrades() + 1

    def setup(self, on_level_up):
        self.on_level_up = on_level_up

    def increase_exp(self, amount):
        if self.level >= self.max_level:
            return
        self.experience += amount
        next_level_exp = self.get_next_level_exp()
        if self.experience >= next_level_exp:
            self.on_level_up()
            self.level += 1
            self.experience = self.experience - next_level_exp
        self.notify_listeners(self)

    def get_level(self):
        return self.level

    def is_max_level(self):
        return self.level >= self.max_level

    def get_exp(self):
        return self.experience

    def get_next_level_exp(self):
        if self.level >= self.max_level:
            return 0
        return MagicLevel.__BASE_TARGET_EXP + MagicLevel.__LEVEL_STEP_EXP * (
            self.level - 1
        )

    def from_model_magic_level(model_magic_level):
        return MagicLevel(
            model_magic_level.level,
            model_magic_level.experience,
        )
