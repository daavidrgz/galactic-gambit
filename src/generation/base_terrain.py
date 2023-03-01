import numpy as np
import pygame
from generation.tile import Tile

from systems.camera_manager import ScrollableGroup
from constants import TILE_SIZE


class BaseTerrain:
    def __init__(self, terrain_size, starting_tile):
        self.sprites = ScrollableGroup()
        self.generation_mask = np.full(terrain_size, False)
        self.ground_mask = np.full(terrain_size, False)
        self.starting_tile = starting_tile
        self.height, self.width = terrain_size

    def clear(self):
        self.sprites.empty()
        self.generation_mask.fill(False)
        self.ground_mask.fill(False)

    def draw(self, screen):
        self.sprites.draw(screen)

    # Template pattern
    def get_wall_tile(self, x, y):
        return Tile(x, y, self.get_wall_sprite())

    def get_ground_tile(self, x, y):
        return Tile(x, y, self.get_ground_sprite())

    def get_wall_sprite(self):
        raise NotImplementedError

    def get_ground_sprite(self):
        raise NotImplementedError

    def on_ground(self, rect):
        starting_x, starting_y = rect.topleft
        rect_width, rect_height = rect.size
        end_x, end_y = starting_x + rect_width, starting_y + rect_height
        logical_starting_x, logical_starting_y = Tile.tile_to_logical_position(
            (starting_x, starting_y)
        )
        logical_end_x, logical_end_y = Tile.tile_to_logical_position((end_x, end_y))
        return self.ground_mask[
            logical_starting_y : logical_end_y + 1,
            logical_starting_x : logical_end_x + 1,
        ].all()

    # TODO
