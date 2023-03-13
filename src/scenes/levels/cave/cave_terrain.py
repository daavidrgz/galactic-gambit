import numpy as np
from constants.game_constants import TILE_SIZE
from generation.base_terrain import BaseTerrain, TerrainType
from generation.tile import Tile
from systems.resource_manager import Resource, ResourceManager


class CaveTerrain(BaseTerrain):
    def populate(self):
        self.data = np.full((171, 171), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = [(84, 3), (85, 3), (86, 3)]

        for x in range(85 - 1, 85 + 2):
            for y in range(0, 3):
                self.data[y, x] = TerrainType.GROUND

        self.player_starting_position = (TILE_SIZE * 85.5, TILE_SIZE * 1.5)

    def place_end(self, end_pos):
        for x in range(end_pos[0] - 7, end_pos[0] + 8):
            for y in range(end_pos[1] - 7, end_pos[1] + 8):
                distance_sqr = (x // 2 * 2 - end_pos[0]) ** 2 + (y // 2 * 2 - end_pos[1]) ** 2
                if distance_sqr < 5**2:
                    self.data[y, x] = TerrainType.GROUND

        self.data[end_pos[1]:end_pos[1]+2, end_pos[0]:end_pos[0]+2] = TerrainType.WALL
        self.end_position = (
            (end_pos[0] + 0.5) * TILE_SIZE,
            (end_pos[1] + 0.5) * TILE_SIZE,
        )
