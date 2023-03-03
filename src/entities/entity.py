import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, hitbox, initial_pos):
        super().__init__()
        self.image = image
        self.image_rect = self.image.get_rect()
        self.rect = hitbox
        self.x, self.y = (round(a) for a in initial_pos)

        self.rect.centerx = self.x
        self.rect.centery = self.y

    def setup(self):
        pass

    def update(self, elapsed_time):
        pass

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = (round(a) for a in position)
        self.rect.centerx, self.rect.centery = self.x, self.y

    def move(self, delta_position):
        deltax, deltay = delta_position
        currentx, currenty = self.get_position()
        self.set_position((currentx + deltax, currenty + deltay))
