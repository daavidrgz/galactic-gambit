from entities.projectile.projectile import Projectile
import pygame


class Bullet(Projectile):
    def __init__(self, initial_pos, speed, direction):
        image = pygame.image.load("assets/sprites/player.png")
        scaled_image = pygame.transform.scale(image, (16, 16))
        hitbox = scaled_image.get_rect()
        super().__init__(scaled_image, hitbox, initial_pos, speed, direction)
