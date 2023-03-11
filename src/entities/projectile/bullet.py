import numpy as np
from animations.explosion_effect import ExplosionEffect
from entities.projectile.projectile import Projectile
from systems.resource_manager import Resource, ResourceManager
import pygame


class Bullet(Projectile):
    def __init__(self, initial_pos, speed, direction, init_upgrades, update_upgrades):
        self.resource_manager = ResourceManager.get_instance()
        image = self.resource_manager.load_image(Resource.LASER)
        image = pygame.transform.scale(image, (60, 20))
        self.update_upgrades = update_upgrades
        super().__init__(image, initial_pos, speed, direction)
        # Apply init upgrades
        [upgrade.apply(self) for upgrade in init_upgrades]

    def collide(self, animation_group):
        explosion_animation = ExplosionEffect(self.get_position())
        animation_group.add(explosion_animation)
        super().collide()

    def update(self, elapsed_time):
        super().update(elapsed_time)
        [upgrade.apply(self, elapsed_time) for upgrade in self.update_upgrades]
