from enum import Enum, auto
import random


class Generator(Enum):
    MAP = auto()
    ENEMIES = auto()
    WEAPON_UPGRADES = auto()
    MAGIC_UPGRADE = auto()


class RngSystem:
    _instance = None

    def get_instance():
        if RngSystem._instance is None:
            RngSystem._instance = RngSystem()
        return RngSystem._instance

    def __init__(self):
        self.__global_rng = random.Random()
        self.__global_rng.seed()
        self.rngs = {}
        self.__initialize_generators()

    def __initialize_generators(self):
        # initialize Generators with a seed generated by the global rng
        for generator in Generator:
            self.rngs[generator] = random.Random(self.__global_rng.randbytes(32))

    def seed(self, seed):
        self.__global_rng.seed(seed)
        self.__initialize_generators()

    def get_rng(self, generator):
        return self.rngs[generator]

    def random(self, generator):
        return self.rngs[generator].random()

    def randbytes(self, generator, n):
        return self.rngs[generator].randbytes(n)
