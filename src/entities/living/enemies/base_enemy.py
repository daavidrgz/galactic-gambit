from entities.living.living_entity import LivingEntity
from scenes.director import Director
from constants import DESIGN_FRAMERATE

import numpy as np

class BaseEnemy(LivingEntity):
    def __init__(self, hp, initial_pos, image, ai): 
        hitbox = image.get_rect()
        self.ai = ai
        self.speed = np.zeros(2)
        self.target = np.zeros(2)
        self.targeting = False
        super().__init__(image, hitbox, initial_pos, hp)

    def setup(self):
        scene = Director().get_scene()
        self.terrain = scene.get_terrain()
        self.player = scene.get_player()

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        self.ai.run(self, self.player, self.terrain)

        if self.targeting:
            direction = self.target - np.array(self.get_position(), dtype=np.float64)
            l = np.linalg.norm(direction)
            direction /= l if l > 0.0 else 1.0
            self.speed = direction * 2.0
        else:
            self.speed = np.zeros(2)

        self.move(self.speed * elapsed_units)

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
