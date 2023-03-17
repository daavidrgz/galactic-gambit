import numpy as np
import pygame
from constants.game_constants import DESIGN_FRAMERATE
from entities.entity import Entity


class Projectile(Entity):
    def __init__(
        self, image, initial_pos, speed, direction, damage, knockback, lifetime
    ):
        self.base_image = image
        super().__init__(image, initial_pos)

        self.velocity = speed * direction
        self.damage = damage
        self.knockback = knockback
        self.ground_collision = True
        self.lifetime = lifetime

        self.previous_facing = 0
        self.set_facing(np.rad2deg(np.arctan2(-direction[1], direction[0])))

    def setup(self, level):
        super().setup(level)

    def collide(self, add_animation_func):
        self.kill()

    def set_facing(self, angle):
        if abs(angle - self.previous_facing) < 5:
            return

        self.previous_facing = angle
        self.set_image(pygame.transform.rotate(self.base_image, angle))

    def get_direction(self):
        return self.velocity / np.linalg.norm(self.velocity)

    def update(self, elapsed_time):
        self.lifetime -= elapsed_time
        if self.lifetime <= 0:
            self.collide(self.level.animation_group.add)

        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000

        self.set_facing(np.rad2deg(np.arctan2(-self.velocity[1], self.velocity[0])))
        self.move(self.velocity * elapsed_units)

        if (
            not self.level.terrain.on_ground_point((self.x, self.y))
            and self.ground_collision
        ):
            self.collide(self.level.animation_group.add)

        super().update(elapsed_time)
