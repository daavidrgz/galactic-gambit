from entities.projectile.projectile import Projectile
from managers.resource_manager import ResourceManager
import pygame


class Bullet(Projectile):
    def __init__(self, initial_pos, direction):
        self.manager = ResourceManager.get_instance()
        image = self.manager.load_image(self.manager.PLAYER)
        scaled_image = pygame.transform.scale(image, (16, 16))
        hitbox = scaled_image.get_rect()

        velocity = direction * 0.1
        super().__init__(scaled_image, hitbox, initial_pos, velocity)
