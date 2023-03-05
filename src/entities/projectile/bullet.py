from entities.projectile.projectile import Projectile
from mechanics.magic.magic_upgrade import DoubleSize
from systems.resource_manager import ResourceManager
import pygame


class Bullet(Projectile):
    def __init__(self, initial_pos, speed, direction, init_upgrades, update_upgrades):
        self.manager = ResourceManager.get_instance()
        image = self.manager.load_image(self.manager.PLAYER)
        scaled_image = pygame.transform.scale(image, (16, 16))
        hitbox = scaled_image.get_rect()
        self.update_upgrades = update_upgrades
        super().__init__(scaled_image, hitbox, initial_pos, speed, direction)
        # Apply init upgrades
        [upgrade.apply(self) for upgrade in init_upgrades]

    def update(self, elapsed_time):
        super().update(elapsed_time)
        [upgrade.apply(self, elapsed_time) for upgrade in self.update_upgrades]
