from systems.rng_system import Generator, RngSystem


class MagicLevel:
    __BASE_TARGET_EXP = 100
    __STEP_EXP = 50

    def __init__(self, initial_level, initial_experience):
        self.level = initial_level
        self.experience = initial_experience
        self.rng = RngSystem.get_instance().get_rng(Generator.MAGIC)

    def next_level_experience(self):
        return MagicLevel.__BASE_TARGET_EXP + MagicLevel.__STEP_EXP * self.level
