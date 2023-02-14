from entities.living.living_entity import LivingEntity
import pygame


class Player(LivingEntity):
    def __init__(self, initial_pos):
        image = pygame.image.load("assets/sprites/player.png")
        hitbox = image.get_rect()
        super().__init__(image, hitbox, initial_pos, 100)

    def update(self, elapsed_time):
        pass
