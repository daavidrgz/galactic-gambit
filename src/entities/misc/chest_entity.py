from entities.entity import Entity
from systems.resource_manager import Resource, ResourceManager
import utils.math

import pygame
import numpy as np


class ChestEntity(Entity):
    def __init__(self, initial_pos):
        image = ResourceManager().load_image(Resource.CHEST)
        image = pygame.transform.scale(image, [x*2 for x in image.get_size()])
        super().__init__(image, initial_pos)

        self.open = False

    def setup(self, level):
        self.player_bullets = level.player_bullets
        super().setup(level)

    def update(self, elapsed_time):
        if self.open:
            return

        for bullet in self.player_bullets:
            if utils.math.circle_rect_collision((bullet.x, bullet.y, bullet.size), self.rect):
                bullet.kill()

                self.open = True
                image = ResourceManager().load_image(Resource.CHEST_OPEN)
                image = pygame.transform.scale(image, [x*2 for x in image.get_size()])
                self.set_image(image)

        super().update(elapsed_time)
