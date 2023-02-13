# Make a enum of directions (UP, DOWN, LEFT, RIGHT)

from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def get_displacement(direction, speed, time):
        return direction.value[0] * speed * time, direction.value[1] * speed * time
