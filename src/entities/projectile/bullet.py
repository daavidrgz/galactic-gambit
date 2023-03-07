import numpy as np
from animations.explosion_animation import ExplosionAnimaton
from entities.projectile.projectile import Projectile
from mechanics.magic.magic_upgrade import DoubleSize
from systems.resource_manager import Resource, ResourceManager
import pygame


class Bullet(Projectile):
    def __init__(self, initial_pos, speed, direction, init_upgrades, update_upgrades):
        self.resource_manager = ResourceManager.get_instance()
        image = self.resource_manager.load_image(Resource.LASER)
        image = pygame.transform.scale(image, (60, 20))
        hitbox = image.get_rect()
        self.update_upgrades = update_upgrades
        super().__init__(image, hitbox, initial_pos, speed, direction)
        # Apply init upgrades
        [upgrade.apply(self) for upgrade in init_upgrades]

    def collide(self, animations):
        explosion_animation = ExplosionAnimaton(self.get_position())
        explosion_animation.play()
        animations.append(explosion_animation)
        super().collide()

    def update(self, elapsed_time):
        super().update(elapsed_time)
        [upgrade.apply(self, elapsed_time) for upgrade in self.update_upgrades]
