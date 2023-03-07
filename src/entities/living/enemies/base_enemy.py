from entities.living.living_entity import LivingEntity
from scenes.director import Director
from constants import DESIGN_FRAMERATE
from systems.rng_system import RngSystem, Generator

import numpy as np


class BaseEnemy(LivingEntity):
    def __init__(self, hp, initial_pos, image, ai):
        hitbox = image.get_rect()
        self.ai = ai
        self.speed = np.zeros(2)
        self.target = np.zeros(2)
        self.targeting = False
        super().__init__(image, hitbox, initial_pos, 0.25, (0, 0, 20), hp)

    def setup(self):
        scene = Director().get_scene()
        self.terrain = scene.get_terrain()
        self.player = scene.get_player()

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        self.ai.run(self, self.player, self.terrain)

        # Movement
        if self.targeting:
            move_vector = self.target - np.array(self.get_position(), dtype=np.float64)
        else:
            move_vector = np.zeros(2)

        vector_norm = np.linalg.norm(move_vector)
        if vector_norm > 0.0:
            move_vector /= vector_norm

        self.velocity += move_vector * 0.7 * elapsed_units

        super().update(elapsed_time)

    def trigger_attack(self):
        pass

    def alerted(self):
        pass

    def set_target(self, point):
        if point is None:
            self.targeting = False
            return

        self.target = point
        self.targeting = True

    def attack(self):
        pass
