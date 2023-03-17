from entities.projectile.projectile import Projectile
from systems.resource_manager import Resource, ResourceManager
from animations.explosion_effect import ExplosionEffect
import utils.math

import pygame


class EnemyBullet(Projectile):
    def __init__(
        self, attack_image, initial_pos, speed, direction, damage, knockback, lifetime
    ):
        resource_manager = ResourceManager.get_instance()
        image = resource_manager.load_image(attack_image)
        image = pygame.transform.scale(image, (50, 10))

        super().__init__(
            image, initial_pos, speed, direction, damage, knockback, lifetime
        )
        self.add_image_modifier(self.__red_image_modifier)

    def collide(self, add_animation_func):
        explosion = ExplosionEffect(self.get_position())
        explosion.add_image_modifier(self.__red_image_modifier)
        add_animation_func(explosion)
        super().collide(add_animation_func)

    def __red_image_modifier(
        self, image
    ):  # TODO: This doesn't need to be dynamic, make it a sprite
        color = (255, 0, 0)
        mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        mask.fill(color)
        mask.set_alpha(30)
        image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def update(self, elapsed_time):
        super().update(elapsed_time)

        # Player collision
        if utils.math.circle_rect_collision(
            (self.x, self.y, 4), self.level.player.rect
        ):
            self.level.player.hit(self.damage, self.get_direction() * self.knockback)
            self.kill()
