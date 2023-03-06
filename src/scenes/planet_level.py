from scenes.level import Level
from generation.base_terrain import BaseTerrain, TerrainType
from generation.generator import BaseGenerator
from systems.resource_manager import ResourceManager
from systems.rng_system import RngSystem, Generator
from generation.tile import Tile

import numpy as np

from constants import TILE_SIZE

class PlanetGenerator(BaseGenerator):
    def __init__(self, terrain):
        self.resource_manager = ResourceManager.get_instance()
        self.dirt_sprite = self.resource_manager.load_tile(self.resource_manager.DIRT)
        self.cobble_sprite = self.resource_manager.load_tile(
            self.resource_manager.COBBLESTONE
        )

        super().__init__(
            (10.0, 10.0),
            (2, 2),
            terrain
        )

    def coordinate_transform(self, x, y):
        x -= 85
        y -= 85
        return (np.sqrt(x*x + y*y), np.arctan2(y, x) * 5)

    def get_wall_sprite(self, x, y):
        return self.cobble_sprite

    def get_ground_sprite(self, x, y):
        return self.dirt_sprite
    
    def noise_wall_condition(self, n, x, y):
        return n < (x / 114)**3

class PlanetTerrain(BaseTerrain):
    def populate(self):
        self.data = np.full((171, 171), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = []

        resource_manager = ResourceManager.get_instance()
        andesite_sprite = resource_manager.load_tile(resource_manager.POLISHED_ANDESITE)
        for x in range(85 - 15, 85 + 16):
            for y in range(85 - 15, 85 + 16):
                distance_sqr = (x - 85)**2 + (y - 85)**2
                if distance_sqr < 11**2:
                    self.data[y, x] = TerrainType.GROUND
                    self.sprites.add(Tile(x, y, andesite_sprite))
                elif distance_sqr < 12**2:
                    self.starting_tiles.append((x, y))

        self.player_starting_position = (TILE_SIZE * 85.5, TILE_SIZE * 85.5)

class PlanetLevel(Level):
    def __init__(self):
        terrain = PlanetTerrain()
        generator = PlanetGenerator(terrain)
        background_color = (40, 30, 20)
        super().__init__(generator, terrain, background_color)
