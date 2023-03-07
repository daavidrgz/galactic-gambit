import numpy as np
import pygame
from constants import DESIGN_FRAMERATE
from entities.entity import Entity


class Projectile(Entity):
    def __init__(self, image, hitbox, initial_pos, speed, direction):
        image = pygame.transform.rotate(
            image, np.rad2deg(np.arctan2(-direction[1], direction[0]))
        )
        super().__init__(image, hitbox, initial_pos)

        self.speed = speed
        self.direction = direction
        self.velocity = speed * direction

    def collide(self):
        self.kill()

    def update(self, elapsed_time):
        elapsed_units = elapsed_time * DESIGN_FRAMERATE / 1000
        delta_position = self.velocity * elapsed_units
        self.move(delta_position)
