import numpy as np
from constants.game_constants import TILE_SIZE
from generation.base_terrain import BaseTerrain, TerrainType
from generation.tile import Tile
from systems.resource_manager import Resource, ResourceManager

import pygame


class CaveTerrain(BaseTerrain):
    def populate(self):
        self.data = np.full((171, 171), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = [(84, 7), (85, 7), (86, 7)]

        # Starting ground and upper wall
        self.data[4:7, 84:87] = TerrainType.GROUND
        self.data[4, 80:90] = TerrainType.WALL

        self.player_starting_position = (TILE_SIZE * 86.0, TILE_SIZE * 5.5)

        self.place_start_sprite(81, 0)

    def place_end(self, end_pos):
        # Make a small area for the end
        for x in range(end_pos[0] - 7, end_pos[0] + 8):
            for y in range(end_pos[1] - 7, end_pos[1] + 8):
                distance_sqr = (x // 2 * 2 - end_pos[0]) ** 2 + (
                    y // 2 * 2 - end_pos[1]
                ) ** 2
                if distance_sqr < 5**2:
                    self.data[y, x] = TerrainType.GROUND

        self.data[
            end_pos[1] : end_pos[1] + 2, end_pos[0] : end_pos[0] + 2
        ] = TerrainType.WALL
        
        self.end_position = (
            (end_pos[0] + 0.5) * TILE_SIZE,
            (end_pos[1] + 0.5) * TILE_SIZE,
        )

    def place_start_sprite(self, x, y):
        image = ResourceManager().load_image(Resource.CAVE_START)
        image = pygame.transform.scale(
            image, [a * 2 for a in image.get_size()]
        )
        self.place_top_sprite(x, y, image)
