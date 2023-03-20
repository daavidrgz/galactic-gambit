from entities.entity import Entity
from utils.math import vector2

import numpy as np

from constants.game_constants import DESIGN_FRAMERATE


class KinematicEntity(Entity):
    def __init__(self, image, initial_pos, drag, collision):
        super().__init__(image, initial_pos)
        self.drag = drag
        self.collision = collision
        self.velocity = np.zeros(2)

    def setup(self, level):
        self.terrain = level.get_terrain()
        super().setup(level)

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        self.velocity -= self.drag * elapsed_units * self.velocity

        collision_offset = vector2(self.collision[0], self.collision[1])
        final_position = self.position + self.velocity * elapsed_units + collision_offset
        pos = self.terrain.get_collision_vector(final_position, self.collision[2])
        self.position = pos - collision_offset

        super().update(elapsed_time)
