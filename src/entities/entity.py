import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, initial_pos):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        x, y = initial_pos
        self.rect.centerx = x
        self.rect.centery = y
