import numpy as np
from animations.explosion_effect import ExplosionEffect
from entities.projectile.projectile import Projectile
from systems.resource_manager import Resource, ResourceManager
import pygame


class PlayerBullet(Projectile):
    def __init__(
        self,
        initial_pos,
        speed,
        direction,
        damage,
        knockback,
        init_upgrades,
        update_upgrades,
    ):
        self.resource_manager = ResourceManager.get_instance()
        image = self.resource_manager.load_image(Resource.LASER)
        image = pygame.transform.scale(image, (60, 20))
        self.update_upgrades = update_upgrades
        super().__init__(image, initial_pos, speed, direction, damage, knockback)
        # Apply init upgrades
        [upgrade.apply(self) for upgrade in init_upgrades]

    def collide(self, add_animation_func):
        add_animation_func(ExplosionEffect(self.get_position()))
        super().collide(add_animation_func)

    def update(self, elapsed_time):
        super().update(elapsed_time)
        [upgrade.apply(self, elapsed_time) for upgrade in self.update_upgrades]

        # Enemy collision
        enemy = pygame.sprite.spritecollideany(self, self.level.enemy_group)
        if enemy is not None:
            enemy.hit(self.damage, self.direction * self.knockback)
            self.kill()
