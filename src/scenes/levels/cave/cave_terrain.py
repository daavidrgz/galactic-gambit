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

        resource_manager = ResourceManager.get_instance()
        andesite_sprite = resource_manager.load_tile(Resource.POLISHED_ANDESITE)
        for x in range(85 - 1, 85 + 2):
            for y in range(0, 3):
                self.data[y, x] = TerrainType.GROUND
                self.sprites.add(Tile(x, y, andesite_sprite))

        self.player_starting_position = (TILE_SIZE * 85.5, TILE_SIZE * 1.5)
