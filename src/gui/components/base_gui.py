import pygame


class BaseGui(pygame.sprite.Sprite):
    def __init__(self, surface, position):
        self.image = surface
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = position
        super().__init__()

    def set_surface(self, surface):
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def set_position(self, position):
        self.rect.center = position

    def set_position_rel(self, position):
        deltax, deltay = position
        self.rect.center = (self.rect.center[0] + deltax, self.rect.center[1] + deltay)

    def is_inside(self, position):
        return self.rect.collidepoint(position)

    def execute_action(self):
        pass
