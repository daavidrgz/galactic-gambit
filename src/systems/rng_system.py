from enum import Enum, auto
import random

from utils.singleton import Singleton


class Generator(Enum):
    MAP = auto()
    ENEMIES = auto()
    PLAYER = auto()
    TECHNOLOGY = auto()
    MAGIC = auto()


class RngSystem(metaclass=Singleton):
    def __init__(self):
        self.__global_rng = random.Random()
        self.__global_rng.seed()
        self.rngs = {}
        self.__seed_generators()

    def __seed_generators(self):
        # initialize Generators with a seed generated by the global rng
        for generator in Generator:
            self.rngs[generator] = random.Random(self.__global_rng.randbytes(32))

    def set_states(self, states):
        for generator, state in states.items():
            self.rngs[generator].setstate(state)

    def get_states(self):
        return {generator: self.rngs[generator].getstate() for generator in Generator}

    def seed(self, seed):
        self.__global_rng.seed(seed)
        self.__seed_generators()

    def get_rng(self, generator):
        return self.rngs[generator]

    def random(self, generator):
        return self.rngs[generator].random()

    def randbytes(self, generator, n):
        return self.rngs[generator].randbytes(n)