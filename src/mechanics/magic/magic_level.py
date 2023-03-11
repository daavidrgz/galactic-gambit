class MagicLevel:
    __BASE_TARGET_EXP = 100
    __LEVEL_STEP_EXP = 50

    def __init__(self, initial_level=0, initial_experience=0):
        self.level = initial_level
        self.experience = initial_experience

    def set_on_level_up(self, on_level_up):
        self.on_level_up = on_level_up

    def increase_experience(self, amount):
        self.experience += amount
        if self.experience >= 20:
            self.on_level_up()
            self.level += 1
            self.experience = 0

    def __next_level_experience(self):
        return MagicLevel.__BASE_TARGET_EXP + MagicLevel.__LEVEL_STEP_EXP * self.level
