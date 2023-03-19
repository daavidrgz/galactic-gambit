from pygame.sprite import Sprite
from constants.game_constants import TILE_SIZE


class Tile(Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = Tile.get_tile_position((x, y))

    def get_tile_position(logical_position):
        return (logical_position[0] * TILE_SIZE, logical_position[1] * TILE_SIZE)

    def tile_to_logical_position(tile_position):
        return (int(tile_position[0] // TILE_SIZE), int(tile_position[1] // TILE_SIZE))
