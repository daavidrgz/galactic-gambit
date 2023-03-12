import pygame
from entities.projectile.projectile import Projectile
from systems.resource_manager import Resource, ResourceManager
from animations.explosion_effect import ExplosionEffect


class EnemyBullet(Projectile):
    def __init__(self, initial_pos, direction):
        self.resource_manager = ResourceManager.get_instance()
        image = self.resource_manager.load_image(Resource.LASER)
        image = pygame.transform.scale(image, (60, 20))

        super().__init__(image, initial_pos, 12, direction, 1)
        self.add_image_modifier(self.__red_image_modifier)

    def collide(self, add_animation_func):
        explosion = ExplosionEffect(self.get_position())
        explosion.add_image_modifier(self.__red_image_modifier)
        add_animation_func(explosion)
        super().collide()

    def __red_image_modifier(self, image):
        color = (255, 0, 0)
        mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        mask.fill(color)
        mask.set_alpha(30)
        image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
