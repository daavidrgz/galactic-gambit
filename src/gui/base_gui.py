import pygame


class BaseGui(pygame.sprite.Sprite):
    def __init__(self, surface, position):
        self.image = surface
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = position
        super().__init__()

    def set_position(self, position):
        self.rect.center = position

    def is_inside(self, position):
        return self.rect.collidepoint(position)

    def action(self):
        pass
