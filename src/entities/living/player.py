from entities.living.living_entity import LivingEntity
import pygame


class Player(LivingEntity):
    def __init__(self, initial_pos):
        image = pygame.image.load("assets/player.png")
        super().__init__(image, initial_pos, 100)
