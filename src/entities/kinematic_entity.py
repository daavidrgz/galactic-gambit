from entities.entity import Entity
from scenes.director import Director

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

        final_position = np.array(
            [
                self.x + self.velocity[0] * elapsed_units + self.collision[0],
                self.y + self.velocity[1] * elapsed_units + self.collision[1],
            ],
            dtype=np.float64,
        )
        pos = self.terrain.get_collision_vector(final_position, self.collision[2])
        self.set_position((pos[0] - self.collision[0], pos[1] - self.collision[1]))

        super().update(elapsed_time)
