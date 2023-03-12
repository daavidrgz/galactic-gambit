import numpy as np
from animations.explosion_effect import ExplosionEffect
from entities.projectile.projectile import Projectile
from systems.resource_manager import Resource, ResourceManager
import pygame


class PlayerBullet(Projectile):
    def __init__(
        self, initial_pos, speed, direction, damage, init_upgrades, update_upgrades
    ):
        self.resource_manager = ResourceManager.get_instance()
        image = self.resource_manager.load_image(Resource.LASER)
        image = pygame.transform.scale(image, (60, 20))
        self.update_upgrades = update_upgrades
        super().__init__(image, initial_pos, speed, direction, damage)
        # Apply init upgrades
        [upgrade.apply(self) for upgrade in init_upgrades]

    def collide(self, add_animation_func):
        add_animation_func(ExplosionEffect(self.get_position()))
        super().collide()

    def update(self, elapsed_time):
        [upgrade.apply(self, elapsed_time) for upgrade in self.update_upgrades]
        super().update(elapsed_time)