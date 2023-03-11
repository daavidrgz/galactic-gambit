from utils.observable import Observable


class MagicLevel(Observable):
    __BASE_TARGET_EXP = 100
    __LEVEL_STEP_EXP = 50

    def __init__(self, initial_level=0, initial_exp=0):
        super().__init__()
        self.level = initial_level
        self.experience = initial_exp

    def setup(self, on_level_up):
        self.on_level_up = on_level_up

    def increase_exp(self, amount):
        self.experience += amount
        next_level_exp = self.get_next_level_exp()
        if self.experience >= next_level_exp:
            self.on_level_up()
            self.level += 1
            self.experience = self.experience - next_level_exp
        self.notify_listeners(self)

    def get_level(self):
        return self.level

    def get_exp(self):
        return self.experience

    def get_next_level_exp(self):
        return MagicLevel.__BASE_TARGET_EXP + MagicLevel.__LEVEL_STEP_EXP * self.level
