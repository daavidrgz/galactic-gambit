import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, hitbox, initial_pos):
        super().__init__()
        self.image = image
        self.image_rect = self.image.get_rect()
        self.rect = hitbox
        self.x, self.y = initial_pos

        # Set to absolute position, for collisions
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self, elapsed_time):
        raise NotImplementedError

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        # TODO: Está bien setear tambien el rect? para las colisiones...
        # pero también queremos tener el self.x y self.y
        self.x, self.y = position
        self.rect.centerx, self.rect.centery = position

    def move(self, delta_position):
        deltax, deltay = delta_position
        currentx, currenty = self.get_position()
        self.set_position((currentx + deltax, currenty + deltay))
