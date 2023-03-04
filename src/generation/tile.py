from pygame.sprite import Sprite
from constants import TILE_SIZE


class Tile(Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.image_rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.topleft = Tile.get_tile_position((x, y))
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def get_tile_position(logical_position):
        return (logical_position[0] * TILE_SIZE, logical_position[1] * TILE_SIZE)

    def tile_to_logical_position(tile_position):
        return (tile_position[0] // TILE_SIZE, tile_position[1] // TILE_SIZE)