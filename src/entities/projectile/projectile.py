import numpy as np
import pygame
from constants.game_constants import DESIGN_FRAMERATE
from entities.entity import Entity


class Projectile(Entity):
    def __init__(self, image, initial_pos, speed, direction, damage, knockback):
        image = pygame.transform.rotate(
            image, np.rad2deg(np.arctan2(-direction[1], direction[0]))
        )
        super().__init__(image, initial_pos)

        self.speed = speed
        self.direction = direction
        self.velocity = speed * direction
        self.damage = damage
        self.knockback = knockback

    def setup(self, level):
        super().setup(level)

    def collide(self, add_animation_func):
        self.kill()

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000
        delta_position = self.velocity * elapsed_units
        self.move(delta_position)

        if not self.level.terrain.on_ground_point((self.x, self.y)):
            self.collide(self.level.animation_group.add)

        super().update(elapsed_time)
