from generation.tile import Tile
from systems.camera_manager import ScrollableGroup
import utils.math

from constants import TILE_SIZE

from enum import IntEnum
import numpy as np
import pygame

class TerrainType(IntEnum):
    NONE = 0

    GROUND = 1
    WALL = 2

    GENERATING = -1
    BOUND = -2

class BaseTerrain:
    def __init__(self, data, starting_tile):
        self.sprites = ScrollableGroup()
        self.data = data
        self.starting_tile = starting_tile
        self.height, self.width = data.shape

    def clear(self):
        self.sprites.empty()
        self.data.fill(0)

    def draw(self, screen):
        self.sprites.draw(screen)

    def on_ground(self, rect):
        starting_x, starting_y = rect.topleft
        rect_width, rect_height = rect.size
        end_x, end_y = starting_x + rect_width, starting_y + rect_height
        logical_starting_x, logical_starting_y = Tile.tile_to_logical_position(
            (starting_x, starting_y)
        )
        logical_end_x, logical_end_y = Tile.tile_to_logical_position((end_x, end_y))
        return (self.data[
            logical_starting_y : logical_end_y + 1,
            logical_starting_x : logical_end_x + 1,
        ] == TerrainType.GROUND).all()

    def get_collision_vector(self, point, distance):
        tile_pos_x, tile_pos_y = Tile.tile_to_logical_position(point)
        tile_pos_x = int(tile_pos_x)
        tile_pos_y = int(tile_pos_y)
        pos = np.array(point, dtype=np.float64)
        for x in range(max(0, tile_pos_x - 1), min(self.width, tile_pos_x + 2)):
            for y in range(max(0, tile_pos_y - 1), min(self.height, tile_pos_y + 2)):
                if self.data[y, x] == TerrainType.GROUND: continue
                r = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pos += utils.math.circle_rect_collision_vector((pos[0], pos[1], distance), r)
        return pos - point
    
    # TODO
