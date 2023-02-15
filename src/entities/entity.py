import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, hitbox, initial_pos):
        super().__init__()
        self.image = image
        self.rect = hitbox
        self.x, self.y = initial_pos

        # Do not update relative position on initialization, on scene init we should
        # call update_relative_position manually. Assume for now that the scroll is
        # at position (0,0), but this should be modified via update_relative_position
        # after scroll in the scene is created
        # TODO: preguntar a suso esto
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self, elapsed_time):
        raise NotImplementedError

    def get_absolute_position(self):
        return self.x, self.y

    def set_absolute_position(self, position):
        self.x, self.y = position

        scrollx, scrolly = self.x - self.rect.centerx, self.y - self.rect.centery
        self.__update_relative_position_raw(scrollx, scrolly)

    def get_relative_position(self):
        return self.rect.centerx, self.rect.centery

    def update_relative_position(self, scroll):
        scrollx, scrolly = scroll.get_scroll()
        self.__update_relative_position_raw(scrollx, scrolly)

    def __update_relative_position_raw(self, scrollx, scrolly):
        self.rect.centerx = self.x - scrollx
        self.rect.centery = self.y - scrolly

    def move_absolute_position(self, delta_position):
        deltax, deltay = delta_position
        currentx, currenty = self.get_absolute_position()
        self.set_absolute_position((currentx + deltax, currenty + deltay))
