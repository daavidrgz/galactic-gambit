from enum import Enum
from scenes.generation_test_scene import GenerationScene

from scenes.one_scene import OneScene

# TODO: fill this enum with the real Level scenes.
class Level(Enum):
    OneLevel = OneScene
    GenerationTest = GenerationScene
