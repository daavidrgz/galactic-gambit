import random
from entities.living.living_entity import LivingEntity
from entities.xp_entity import XpEntity
from scenes.director import Director
from constants.game_constants import DESIGN_FRAMERATE

import numpy as np

from systems.resource_manager import Resource
from systems.sound_controller import CycleSounds


class BaseEnemy(LivingEntity):
    def __init__(self, hp, initial_pos, image, ai):
        self.ai = ai
        self.speed = np.zeros(2)
        self.target = np.zeros(2)
        self.targeting = False

        super().__init__(image, initial_pos, 0.25, (0, 0, 20), hp)

    def setup(self, level):
        self.player = level.get_player()

        death_sounds = [
            Resource.ALIEN_DEATH_SOUND_01,
            Resource.ALIEN_DEATH_SOUND_02,
            Resource.ALIEN_DEATH_SOUND_03,
        ]
        super().setup(
            level,
            hit_sound=Resource.ALIEN_HIT_SOUND,
            death_sound=random.choice(death_sounds),
        )

    def on_death(self):
        super().on_death()
        self.kill()
        for _ in range(3):
            self.level.spawn_misc_entity(XpEntity((self.x, self.y)))

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        self.ai.run(self, self.player, self.terrain, elapsed_time)

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

    def get_target(self):
        if not self.targeting:
            return None
        return self.target

    def attack(self):
        pass
