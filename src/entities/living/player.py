from entities.living.living_entity import LivingEntity
from managers.resource_manager import ResourceManager
import pygame


class Player(LivingEntity):
    def __init__(self, initial_pos):
        self.manager = ResourceManager.get_instance()
        image = self.manager.loadImage(self.manager.PLAYER)
        hitbox = image.get_rect()
        super().__init__(image, hitbox, initial_pos, 100)

    def update(self, elapsed_time):
        pass
