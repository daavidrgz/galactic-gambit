import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, initial_pos):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        x, y = initial_pos
        self.rect.centerx = x
        self.rect.centery = y

    def update(self, elapsed_time):
        raise NotImplementedError

    def get_position(self):
        return self.rect.centerx, self.rect.centery

    def set_position(self, position):
        x, y = position
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, delta_position):
        x, y = delta_position
        self.rect.centerx += x
        self.rect.centery += y
